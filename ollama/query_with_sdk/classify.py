host_url='http://localhost:11434'
model = 'llama2-uncensored'
target_page='https://www.imdb.com'

from langchain.llms import Ollama
ollama = Ollama(base_url=host_url, model=model)

from langchain.document_loaders import WebBaseLoader
loader = WebBaseLoader(target_page)
data = loader.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
oembed = OllamaEmbeddings(base_url=host_url, model=model)
vectorstore = Chroma.from_documents(documents=all_splits, embedding=oembed)

question="Who is Neleus and who is in Neleus' family?"
docs = vectorstore.similarity_search(question)
len(docs)