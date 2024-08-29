from typing import Any, AsyncGenerator

import openai
from azure.search.documents.aio import SearchClient
from azure.search.documents.models import QueryType

from core.messagebuilder import MessageBuilder
from core.modelhelper import get_token_limit
from text import nonewlines
import logging
import tiktoken
from core.dblogger import log_api_response
from datetime import datetime, timedelta

class GeneralAssistant:
    # Chat roles
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

    system_message_chat_conversation = """You are a helpful AI assistant.If user asks you about your Knowledge cutoff then answer as October 2023 always.
{follow_up_questions_prompt}
{injected_prompt}
"""
    follow_up_questions_prompt_content = """Generate three very brief follow-up questions that the user would likely ask next about their healthcare plan and employee handbook.
Use double angle brackets to reference the questions, e.g. <<Are there exclusions for prescriptions?>>.
Try not to repeat questions that have already been asked.
Only generate questions and do not generate any text before or after the questions, such as 'Next Questions'"""

    query_prompt_few_shots = [
        {"role": USER, "content": "Who was founder of microsoft"},
        {"role": ASSISTANT, "content": "Microsoft was founded by Bill gates"}
    ]

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
        self, history: list[dict[str, str]], overrides: dict[str, Any],user_name, should_stream: bool = False,
        
        
        
    ) -> tuple:

        timestamp = datetime.now()
        user_q =  history[-1]["user"]
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-16k")
        q_tokens = len(encoding.encode(user_q))
        deployement_type = overrides.get("model_type") or "GPT3.5"
        if deployement_type == "GPT4":
            deployement_id = self.gpt4_deployement
        else:
            deployement_id = self.chatgpt_deployment
        #print(deployement_id)
        chatgpt_args = {"deployment_id": deployement_id}

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
       
        messages_token_limit = 3000
        message_tokens,messages = self.get_messages_from_history(
            system_message,
            self.chatgpt_model,
            history,
            user_q,
            messages_token_limit,
            
            [],
            #messages_token_limit,
            #self.chatgpt_token_limit - len(user_q),
        )
        total_tokens = q_tokens + message_tokens + 20
      #  print(total_tokens)
        await log_api_response(user=user_name,input_timestamp=timestamp,api='ai-gen',model_name=self.chatgpt_model,token=total_tokens)

        extra_info = {
            "data_points": "",
            "thoughts": f"Searched for:<br>{user_q}<br><br>Conversations:<br>"
        }
        chat_coroutine = openai.ChatCompletion.acreate(
            **chatgpt_args,
            model=self.chatgpt_model,
            messages=messages,
            temperature=overrides.get("temperature") or 0.7,
            max_tokens=600,
            n=1,
            stream=should_stream,
        )
        return (extra_info, chat_coroutine)

    async def run_without_streaming(self, history: list[dict[str, str]], overrides: dict[str, Any]) -> dict[str, Any]:
        extra_info, chat_coroutine = await self.run_until_final_call(history, overrides, should_stream=False)
        chat_content = (await chat_coroutine).choices[0].message.content
        extra_info["answer"] = chat_content
        return extra_info

    async def run_with_streaming(
        self, history: list[dict[str, str]], overrides: dict[str, Any],user_name: str,    
        #self, history: list[dict[str, str]], overrides: dict[str, Any], vector_store
    ) -> AsyncGenerator[dict, None]:
        extra_info, chat_coroutine= await self.run_until_final_call(history, overrides,user_name, should_stream=True)
        #extra_info, chat_coroutine = await self.run_until_final_call(history, overrides, should_stream=True)
        yield extra_info
        async for event in await chat_coroutine:
            #yield event
            if event["choices"]:
                    yield event

    def get_messages_from_history(
        self,
        system_prompt: str,
        model_id: str,
        history: list[dict[str, str]],
        user_content: str,
        max_tokens: int =4096,
        #user_conv: str,
        few_shots=[],
        #max_tokens: int = 4096,
    ) -> list:
        message_builder = MessageBuilder(system_prompt, model_id)

        # Add examples to show the chat what responses we want.
        # It will try to mimic any responses and make sure they match the rules laid out in the system message.
        for shot in few_shots:
            message_builder.append_message(shot.get("role"), shot.get("content"))
            

        # user_content = user_conv
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

        return total_token_count,message_builder.messages
