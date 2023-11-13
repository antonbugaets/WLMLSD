from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

from langchain.document_loaders import TextLoader

from dotenv import load_dotenv

load_dotenv(".env")

loader = TextLoader("data.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings)

qa = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=docsearch.as_retriever(search_kwargs={"k": 1}),
)

user_phrase = "cute dog"

query = f"Give me one good prompts for Stable Diffusion, using prompt '{user_phrase}'"
result = qa.run(query)

print(result)
