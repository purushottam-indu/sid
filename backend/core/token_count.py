import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredPDFLoader, PyPDFLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import UnstructuredPowerPointLoader

import tiktoken


def token_counter(file):
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY_East")
    AZURE_OPENAI_SERVICE = os.getenv("AZURE_OPENAI_SERVICE_East")
    openai_api_type = "azure"
    openai_api_version = "2023-12-01-preview" 
    openai_api_base = f"https://{AZURE_OPENAI_SERVICE}.openai.azure.com" 
    openai_api_key = AZURE_OPENAI_API_KEY
    embeddings = OpenAIEmbeddings(openai_api_base = openai_api_base,
                              openai_api_type = "azure",
                              openai_api_key=openai_api_key, 
                              openai_api_version = openai_api_version, 
                              deployment="text-embedding-ada-002", 
                              chunk_size = 1)
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

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000,chunk_overlap  = 200)
    docs = text_splitter.split_documents(doc)
    input_str = ""
    enc = tiktoken.encoding_for_model("text-embedding-ada-002")
    for i in range(len(docs)):
        input_str = input_str + docs[i].page_content
    
    return len(enc.encode(input_str)) 

