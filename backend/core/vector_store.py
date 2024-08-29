import openai
import os
import pandas as pd
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredPDFLoader, PyPDFLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import UnstructuredPowerPointLoader

import os
import tiktoken
from .dblogger import log_api_response
from datetime import datetime, timedelta
from typing import Any, AsyncGenerator
from quart import session


count = 0

async def create_vectorstore(file, user_name):
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY_East")
    AZURE_OPENAI_SERVICE = os.getenv("AZURE_OPENAI_SERVICE_East")
    openai_api_type = "azure"
   # openai_api_version = "2023-03-15-preview"
    openai_api_version = "2023-12-01-preview"  
    openai_api_base = f"https://{AZURE_OPENAI_SERVICE}.openai.azure.com" 
    openai_api_key = AZURE_OPENAI_API_KEY
    embeddings = OpenAIEmbeddings(openai_api_base = openai_api_base,
                              openai_api_type = "azure",
                              openai_api_key=openai_api_key, 
                              openai_api_version = openai_api_version, 
                              deployment="text-embedding-ada-002", 
                              #chunk_size = 1,
                            #   max_retries = 0)
                                )
    if file.endswith('.pdf'):
        loader = PyPDFLoader(file)
        doc = loader.load()
    if file.endswith('.txt'):
        loader = TextLoader(file)
        doc = loader.load()
    if file.endswith('.docx'):
        loader = Docx2txtLoader(file)
        doc = loader.load()
    if file.endswith('.pptx'):
        loader = UnstructuredPowerPointLoader(file)
        doc = loader.load()

   # print("Doc Created")
    global count
    count += 1

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000,chunk_overlap  = 200)
    docs = text_splitter.split_documents(doc)
    # print("Docs created", docs)
    
    timestamp = datetime.now()
    enc = tiktoken.encoding_for_model("text-embedding-ada-002")
    input_str = ""
    for i in range(len(docs)):
        input_str = input_str + docs[i].page_content
    embedding_tokens = len(enc.encode(input_str))
   # print("embedding_tokens", embedding_tokens) 
    await log_api_response(user=session['user_name'],input_timestamp=timestamp,api='ai-gen',model_name="text-embedding-ada-002",token=embedding_tokens)

    vector_store = FAISS.from_documents(documents=docs, embedding=embeddings)
 #   print("vector_store created", vector_store)
    path = os.path.join("vector_stored", user_name, "faiss_index_{}".format(count))

    vector_store.save_local(path)

