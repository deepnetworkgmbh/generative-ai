from langchain.prompts import ChatPromptTemplate, PromptTemplate, SystemMessagePromptTemplate

# Used to condense a question and chat history into a single question
query_message = """
Below is the chat history so far, and a new question asked by the user that needs to be answered by searching a knowledge.
You have access to an ElasticSearch index with 100's of documents.
Generate a search query based on the chat history and the new question while obeying all of the following.
- Do not include cited source filenames and document names e.g info.txt or doc.pdf in the search query terms.
- Do not include any text inside [] or <<>> in the search query terms.
- Do not include any special characters like '+'.
- Search query must be human readable.

Chat History:
{chat_history}
New Question: {question}
"""  
GET_QUERY_PROMPT = PromptTemplate.from_template(
    query_message
)

# RAG Prompt to provide the context and question for LLM to answer
# We also ask the LLM to cite the source of the passage it is answering from
llm_context_prompt_template = """
Below are the passages, chat history and the question.
Answer the question ONLY with the facts listed in the passages below. If there isn't enough information below, say you don't know. Do not generate answers that don't use the sources below. If asking a clarifying question to the user would help, ask the question.
Each passage has a SOURCE and PAGE. Always include the source name and page number for each fact you use in the response. Use square brackets to reference the source, for example [info1.txt/page 2]. Don't combine sources, list each source separately, for example [info1.txt/page 1][info2.pdf/page 8].
----
{passages}
----
Chat History:
{chat_history}
Question: {question}
"""

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
