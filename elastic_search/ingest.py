import os

from langchain.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings, AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.elasticsearch import ElasticsearchStore
from rag_elasticsearch.connection import es_connection_details

loader = PyPDFDirectoryLoader(f"{os.getcwd()}/elasticsearch/pdf-data")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(loader.load())

embeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT"),
    openai_api_version="2023-09-01-preview",
)
"""
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2", 
    model_kwargs={"device": "cpu"}
)
"""

# Add to vectorDB
vectorstore = ElasticsearchStore.from_documents(
    documents=all_splits,
    embedding = embeddings,
    **es_connection_details,
    index_name="demo-ada-example",
)
