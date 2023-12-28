from operator import itemgetter
from typing import List, Optional, Tuple
import os

from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import HuggingFaceEmbeddings, AzureOpenAIEmbeddings
from langchain.schema import BaseMessage, format_document
from langchain.vectorstores.elasticsearch import ElasticsearchStore
from langchain_core.output_parsers import StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string
from langchain.globals import set_debug

from .connection import es_connection_details
from .prompts import GET_QUERY_PROMPT, DOCUMENT_PROMPT, LLM_CONTEXT_PROMPT

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

# Setup connecting to Elasticsearch
vectorstore = ElasticsearchStore(
    **es_connection_details,
    embedding=embeddings,
    index_name="demo-ada-example",
)
retriever = vectorstore.as_retriever()

# Set up LLM to user
llm = AzureChatOpenAI(
    openai_api_version="2023-09-01-preview",
    azure_deployment=os.getenv("AZURE_OPENAI_GPT_DEPLOYMENT"),
    temperature=0
    )

def _combine_documents(
    docs, document_prompt=DOCUMENT_PROMPT, document_separator="\n\n"
):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)

_inputs = RunnableParallel(
    query=RunnablePassthrough.assign(
        chat_history=lambda x: get_buffer_string(x["chat_history"], "User", "Assistant")
    )
    | GET_QUERY_PROMPT
    | llm
    | StrOutputParser(),
    passed=RunnablePassthrough()
)

_context = {
    "passages": itemgetter("query") | retriever | _combine_documents,
    "question": lambda x: x["passed"]["question"],
    "chat_history": lambda x: x["passed"]["chat_history"]
}

#set_debug(True)

chain = _inputs | _context | LLM_CONTEXT_PROMPT | llm | StrOutputParser()