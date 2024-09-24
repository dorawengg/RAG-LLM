import streamlit as st
import random
import time
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
# Make sure to import the Ollama package
from langchain_community.llms import Ollama

# Streamed response emulator for testing


def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.02)


st.title("Local medical RAG-LLM Chatbot")

# Retrieve documents
documents = ["articles.pdf"]


@st.cache_data
def load_documents(document_paths):
    docs = []
    for path in document_paths:
        loader = PyPDFLoader(path)
        docs.extend(loader.load())
    return docs


@st.cache_data
def create_faiss_index(_docs):
    embeddings = HuggingFaceEmbeddings()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    chunks = splitter.split_documents(_docs)
    texts = [chunk.page_content for chunk in chunks]
    vector_store = FAISS.from_texts(texts, embeddings)
    return vector_store


# Load and index documents
docs = load_documents(documents)
vector_store = create_faiss_index(docs)

# Set up retriever
retriever = vector_store.as_retriever()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Retrieve relevant documents and generate LLM response
    context = retriever.get_relevant_documents(prompt)
    combined_context = " ".join([doc.page_content for doc in context])
    inputs = f"Context: {combined_context}\n\nQuestion: {prompt}\n\nAnswer:"

    # Replace with actual model name and initialization
    llm = Ollama(model="llama3")
    response = llm.invoke(inputs)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
