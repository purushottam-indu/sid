from typing import Any, AsyncGenerator

import openai
from azure.search.documents.aio import SearchClient
from azure.search.documents.models import QueryType

from core.messagebuilder import MessageBuilder
from core.modelhelper import get_token_limit

# from core.csv_sql import sql_approach
from core.csv_excel_sql import csv_exc_sql

from text import nonewlines
#import pypdf
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
import os
import openpyxl as xl
import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback

import tiktoken
from core.dblogger import log_api_response
from datetime import datetime, timedelta
import re

class DocumentQnA:
    # Chat roles
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

    system_message_chat_conversation = """
    You are a helpful AI assistant that answers the user question using the context provided by the user. Do not justify your answers. Do not give information not mentioned in the context, but you can translate the context into any language if asked.
{injected_prompt}
"""
#{follow_up_questions_prompt}

#     follow_up_questions_prompt_content = """Generate three very brief follow-up questions that the user would likely ask next about their healthcare plan and employee handbook.
# Use double angle brackets to reference the questions, e.g. <<Are there exclusions for prescriptions?>>.
# Try not to repeat questions that have already been asked.
# Only generate questions and do not generate any text before or after the questions, such as 'Next Questions'"""


    def __init__(
        self,
        chatgpt_deployment: str,
        gpt4_deployement: str,
    ):
        self.chatgpt_deployment = chatgpt_deployment
        self.gpt4_deployement = gpt4_deployement
        self.chatgpt_model = "GPT4o"
        self.chatgpt_token_limit = get_token_limit(self.chatgpt_model)

    async def run_until_final_call(
        self, user_name, history: list[dict[str, str]], overrides: dict[str, Any], should_stream: bool = False
    ) -> tuple:
        user_q =  history[-1]["user"]
     #   print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

        AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY_East")
        AZURE_OPENAI_SERVICE = os.getenv("AZURE_OPENAI_SERVICE_East")
        openai_api_version = "2023-12-01-preview" 
        # openai_api_version = "2023-12-01-preview"
        openai_api_base = f"https://{AZURE_OPENAI_SERVICE}.openai.azure.com" 
        openai_api_key = AZURE_OPENAI_API_KEY
        embeddings = OpenAIEmbeddings(openai_api_base = openai_api_base,
                            openai_api_type = "azure",
                            openai_api_key=openai_api_key, 
                            openai_api_version = openai_api_version, 
                            deployment="text-embedding-ada-002", 
                            #chunk_size = 16,
                            # max_retries = 0)
                                     )

        ## For handling CSV & Excel Files
        tempdir = "./tempfile"
        files = os.listdir(os.path.join(tempdir, user_name))
      #  print(len(files), "length of files")
        flag = False
        if len(files)>0:
            os.environ["OPENAI_API_KEY"] = openai_api_key  
            agent_output = ""
            for file in files:
                #agent_output, tokens_consumed_sql = csv_exc_sql().sql_approach(user_q, os.path.join(tempdir,user_name,file), user_name)
                agent_output, tokens_consumed_sql, user_q = csv_exc_sql().sql_approach(user_q, os.path.join(tempdir,user_name,file), user_name)
            # print("-------------------------------------")
            # print("Agent_Output",agent_output)
            # print("-------------------------------------")

            # print(type(agent_output), tokens_consumed_sql)
            tokens_consumed_descriptive = 0
            if type(agent_output) == str:
                if "Please specify sheetname from" in agent_output:
                    response = agent_output
                
                elif agent_output == "Agent stopped due to iteration limit or time limit.":
                    agent_output = """You might have asked something out of the context with the uploaded data, If not please be more specific in the input asked"""
                    response = agent_output

                elif agent_output == """You might have asked something out of the context with the uploaded data, If not please be more specific in the input asked""":
                    response = agent_output     

                else:
                    if "<|im_end|>" in agent_output:
                        agent_output = agent_output.replace("<|im_end|>", "")

                    response, tokens_consumed_descriptive = self.api_call(user_q, agent_output)
            else:
                response, tokens_consumed_descriptive = self.api_call(user_q, agent_output)

            # print("-------------------------------------")
            # print("Descriptive Output",response)
            # print("tokens_consumed_descriptive", tokens_consumed_descriptive, "tokens_consumed_sql", tokens_consumed_sql, "total_tokens", tokens_consumed_descriptive+tokens_consumed_sql)
            # print("-------------------------------------")

            json_output = {
                        "choices": [
                            {
                            "finish_reason": "null",
                            "index": 0,
                            "delta": {
                                "content": response
                            }
                            }
                                    ]
                                }
            flag = True
            timestamp = datetime.now()
            await log_api_response(user=user_name,input_timestamp=timestamp,api='ai-gen',model_name="GPT4o",token=tokens_consumed_descriptive+tokens_consumed_sql)
            return ({},json_output, flag)

        else:
            vector_dict = {}

            folder = os.path.join("vector_stored", user_name)
            folders = os.listdir(folder)
            
            for i, j in enumerate(folders):
                folder_path = os.path.join(folder, j)
               # print(folder_path)
                vector_dict[f"vector_store_{i}"] = FAISS.load_local(folder_path, embeddings=embeddings)
                if i == 0:
                    vector_store = vector_dict[f"vector_store_{i}"]
                else:
                    vector_store.merge_from(vector_dict[f"vector_store_{i}"])
                    
         #   for key, value in vector_dict.items():
            #    print(key, value)


          #  print("vectore_store_loaded", vector_store)
            docs = vector_store.similarity_search(user_q, k = 4)
          #  print("docs created in docuqna", docs)
            context = ""
            for doc in docs:
                context = context + "\n" + doc.page_content
            # print("context created", context)

            user_q = f"""Use the below context only to answer the question. Consider only the provided context to generate the answer.
            <Context>
            {context}
            </Context>

            <Question>
            {user_q}
            </Question>
            """


            deployement_type = overrides.get("model_type") or "GPT3.5"
            if deployement_type == "GPT4":
                deployement_id = self.gpt4_deployement
            else:
                deployement_id = self.chatgpt_deployment

            chatgpt_args = {"deployment_id": deployement_id}

            if deployement_type == "GPT4":
                encoding_model = "gpt-4"
            else:
                encoding_model = "gpt-3.5-turbo"

            encoding = tiktoken.encoding_for_model(encoding_model)
            q_tokens = len(encoding.encode(user_q))     
           # print(q_tokens, "tokens_q") 

            follow_up_questions_prompt = (
                self.follow_up_questions_prompt_content if overrides.get("suggest_followup_questions") else ""
            )

            # # STEP 3: Generate a contextual and content specific answer using the search results and chat history

            # # Allow client to replace the entire prompt, or to inject into the exiting prompt using >>>
            prompt_override = overrides.get("prompt_template")
            if prompt_override is None:
                system_message = self.system_message_chat_conversation.format(
                    injected_prompt="", follow_up_questions_prompt=follow_up_questions_prompt
                )
            else :
                system_message = self.system_message_chat_conversation.format(
                    injected_prompt=prompt_override[3:] + "\n", follow_up_questions_prompt=follow_up_questions_prompt
                )

            docuqna_tokens, messages = self.get_messages_from_history(
                system_message,
                self.chatgpt_model,
                history,
                user_q,
                [],
                self.chatgpt_token_limit - len(user_q),
            )

           # print("docu_tokens", docuqna_tokens)
            total_tokens= q_tokens + docuqna_tokens +20
            timestamp = datetime.now()
            await log_api_response(user=user_name,input_timestamp=timestamp,api='ai-gen',model_name='GPT4o',token=total_tokens)

            extra_info = {
                "data_points": "",
                "thoughts": f"Searched for:<br>{user_q}<br><br>Conversations:<br>"
            }
          #  print("--------------model_type-----------------------------")
          #  print(chatgpt_args, self.chatgpt_model, overrides.get("temperature"))
            chat_coroutine = openai.ChatCompletion.acreate(
                **chatgpt_args,
                model=self.chatgpt_model,
                messages=messages,
                temperature=overrides.get("temperature") or 0.7,
                max_tokens=1024,
                n=1,
                stream=should_stream,
            )
            

            
            return (extra_info, chat_coroutine, flag)

    # async def run_without_streaming(self, history: list[dict[str, str]], overrides: dict[str, Any],vector_store) -> dict[str, Any]:
    #     extra_info, chat_coroutine = await self.run_until_final_call(vactor,history, overrides,should_stream=False)
    #     chat_content = (await chat_coroutine).choices[0].message.content
    #     extra_info["answer"] = chat_content
    #     print("extra_info", extra_info)
    #     return extra_info

    async def run_with_streaming(self,
        history: list[dict[str, str]], overrides: dict[str, Any],user_name
    ) -> AsyncGenerator[dict, None]:
        extra_info, chat_coroutine, flag = await self.run_until_final_call(user_name,history, overrides, should_stream=True)
      #  print("chat_coroutine created", chat_coroutine)
        yield extra_info
        if flag:
            yield chat_coroutine
        else:
            async for event in await chat_coroutine:
                # yield event
            # async for event in await chat_coroutine:
                if event["choices"]:
                    yield event

    def get_messages_from_history(
        self,
        system_prompt: str,
        model_id: str,
        history: list[dict[str, str]],
        user_conv: str,
        few_shots=[],
        max_tokens: int = 4096,
    ) -> list:
        message_builder = MessageBuilder(system_prompt, model_id)

        # Add examples to show the chat what responses we want.
        # It will try to mimic any responses and make sure they match the rules laid out in the system message.
        for shot in few_shots:
            message_builder.insert_message(shot.get("role"), shot.get("content"))

        user_content = user_conv
        append_index = len(few_shots) + 1

        # message_builder.append_message(self.USER, user_content, index=append_index)

        # for h in reversed(history[:-1]):
        #     if bot_msg := h.get("bot"):
        #         message_builder.append_message(self.ASSISTANT, bot_msg, index=append_index)
        #     if user_msg := h.get("user"):
        #         message_builder.append_message(self.USER, user_msg, index=append_index)
        #     if message_builder.token_length > max_tokens:
        #         break

        # messages = message_builder.messages
        # return messages
        message_builder.insert_message(self.USER, user_content, index=append_index)
        total_token_count = message_builder.count_tokens_for_message(message_builder.messages[-1])

        newest_to_oldest = list(reversed(history[:-1]))
        for message in newest_to_oldest:
            potential_message_count = message_builder.count_tokens_for_message(message)
         #   print(message)
            if (total_token_count + potential_message_count) > max_tokens:
                #logging.debug("Reached max tokens of %d, history will be truncated", max_tokens)
                break
            if user_msg := message.get("user"):
                message_builder.insert_message(self.USER, user_msg, index=append_index)
            if bot_msg := message.get("bot"):
                message_builder.insert_message(self.ASSISTANT, bot_msg, index=append_index)

            total_token_count += potential_message_count
        return (total_token_count,message_builder.messages)
    
    
    def api_call(self, user_q, agent_output):
        try:
            user_prompt = """
                        Question : {}
                        
                        Answer : {}""".format(user_q, agent_output)

          #  print(user_prompt)
            
            response = openai.ChatCompletion.create(
                engine = "GPT4o",
                messages = [
                    {"role": "system", "content": """   
                                                    You are provided with the question and answer. 
                                                    Provide the answer as per the question. Examples are present under <Metadata> tag.                                             
                                                    Answer can be a value, dataframe, series, etc. 
                    
                                                    Most Important do not include any words in the response like "Answers:", "Answer:", "Results:", "Response:" etc. 

                                                    <Metadata>
                                                    Consider the below examples, provide such type of responses for the question and answer provided.
                                                    example :- 
                    
                                                    Question:- How many people are married.
                                                    Answer :- 2563
                                                    Response :- 2563 people are married.

                                                    Question :- how many people are there having T Stage less than T3, how many are having T stage as T2 and how many are married
                                                    Answer :- 3389, 1786, 1140
                                                    Response :- 3389 people are having T stage less than T3, 1786 are hacing T stage as T2, 1140 are having T stage T2 and are married.

                    
                                                    Question:- Average tumor size of married people.
                                                    Answer :- 30.87
                                                    Response :- Average tumor size for married people is 30.87
                    
                                                    Question :- Name all the unique countries present in sheet2
                                                    Answer :- india, australia, new zealand
                                                    Response: Here are the names of unique countries in sheet2 india, australia, new zealand.
                    
                                                        """},
                    {"role": "user", "content": user_prompt}
                ]
                )
            return(response['choices'][0]['message']['content'], response["usage"]["total_tokens"])
        except:
            return("""You might have asked something out of the context with the uploaded data, If not please be more specific in the input asked""", 0)
