import os

from langchain.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings, AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.elasticsearch import ElasticsearchStore

ELASTIC_CLOUD_ID = os.getenv("ELASTIC_CLOUD_ID")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME", "elastic")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ES_URL = os.getenv("ES_URL", "http://localhost:9200")

if ELASTIC_CLOUD_ID and ELASTIC_USERNAME and ELASTIC_PASSWORD:
    es_connection_details = {
        "es_cloud_id": ELASTIC_CLOUD_ID,
        "es_user": ELASTIC_USERNAME,
        "es_password": ELASTIC_PASSWORD,
    }
else:
    es_connection_details = {"es_url": ES_URL}

loader = PyPDFDirectoryLoader(f"{os.getcwd()}/elasticsearch/pdf-data")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(loader.load())

embeddings = AzureOpenAIEmbeddings(
    azure_endpoint="https://openai-dn.openai.azure.com",
    azure_deployment="ada-embedding",
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
