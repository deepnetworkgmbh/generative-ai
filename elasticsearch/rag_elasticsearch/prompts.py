from langchain.prompts import ChatPromptTemplate, PromptTemplate

# Used to condense a question and chat history into a single question
condense_question_prompt_template = """
Below is a history of the chat so far, and a new question asked by the user that needs to be answered by searching in a knowledge.
You have access to ElasticSearch index with 100's of documents.
Generate a search query based on the chat and the new question.
Do not include cited source filenames and document names e.g info.txt or doc.pdf in the search query terms.
Do not include any text inside [] or <<>> in the search query terms.
Do not include any special characters like '+'.
If the question is not in English, translate the question to English before generating the search query.
Do not include "Search Query:" in the beginning of the answer.

Chat History:
{chat_history}
New Question: {question}
"""  # noqa: E501
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(
    condense_question_prompt_template
)

# RAG Prompt to provide the context and question for LLM to answer
# We also ask the LLM to cite the source of the passage it is answering from
llm_context_prompt_template = """
Use the following passages to answer the user's question.
Each passage has a SOURCE which is the title of the document. When answering, cite source name of the passages you are answering from below the answer in a unique bullet point list.

If you don't know the answer, just say that you don't know, don't try to make up an answer.

----
{context}
----
Question: {question}
"""  # noqa: E501

LLM_CONTEXT_PROMPT = ChatPromptTemplate.from_template(llm_context_prompt_template)

# Used to build a context window from passages retrieved
document_prompt_template = """
---
SOURCE: {source}
PAGE: {page}
PASSAGE:
{page_content}
---
"""

DOCUMENT_PROMPT = PromptTemplate.from_template(document_prompt_template)
