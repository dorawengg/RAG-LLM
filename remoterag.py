import streamlit as st
from langchain_community.llms import Ollama
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import AgentType, initialize_agent
from langchain.callbacks.manager import CallbackManager
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

st.title("RAG System with Local LLM")

prompt = st.text_input("Prompt:", value="", key="prompt")

# documents = [
#     "Big Companies Find a Way to Identify A.I. Data They Can Trust - The New York Times.pdf"
# ]

# Path to the folder containing your documents
folder_path = '/path/to/your/folder'

# Automatically get a list of all files in the folder
documents = [file for file in os.listdir(folder_path) if file.endswith('.pdf')]


@st.cache_data
def load_documents(document_paths):
    docs = []
    for path in document_paths:
        loader = PyPDFLoader(path)
        docs.extend(loader.load())
    return docs

# Loading documents and casheing data in faiss index


@st.cache_data
def create_faiss_index(_docs):
    embeddings = HuggingFaceEmbeddings()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    chunks = splitter.split_documents(_docs)
    texts = [chunk.page_content for chunk in chunks]
    vector_store = FAISS.from_texts(texts, embeddings)
    return vector_store


# Load and index documents
docs = load_documents(document_paths=documents)
vector_store = create_faiss_index(docs)

# Set up retriever
retriever = vector_store.as_retriever()

# If prompt is not empty, process the input
if prompt:
    response = ""
    llm = Ollama(model="llama3")

    # Use updated invoke method instead of get_relevant_documents
    context = retriever.invoke(prompt)
    combined_context = " ".join([doc.page_content for doc in context])
    inputs = f"Context: {combined_context}\n\nQuestion: {prompt}\n\nAnswer:"
    response = llm.invoke(inputs)

    st.markdown(response)

# $ streamlit run remoterag.py
