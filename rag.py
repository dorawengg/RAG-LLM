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
from langchain.embeddings import HuggingFaceEmbeddings

# Streamlit app title
st.title("RAG System with Local LLM")

# User input section
search_internet = st.checkbox("Check internet?", value=False, key="internet")
prompt = st.text_input("Prompt:", value="", key="prompt")

# Document retrieval setup
# Add paths to your documents
documents = ["./pdfs/Draft 6 The Future of Nursing Documentation (1).pdf",
             #  "./pdfs/71763-gale-encyclopedia-of-medicine.-vol.-1.-2nd-ed.pdf", "./pdfs/Bacterial_Organisms.pdf", "./pdfs/Infection_Disease.pdf",
             #  "./pdfs/Pharmacodynamics_of_Antibacterial_Agents.pdf", "./pdfs/antibacterial_agents.pdf", "./pdfs/drug_usage_dosing.pdf"
             ]


def load_documents(document_paths):
    docs = []
    for path in document_paths:
        loader = PyPDFLoader(path)
        docs.extend(loader.load())
    return docs


def create_faiss_index(docs):
    embeddings = HuggingFaceEmbeddings()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    chunks = splitter.split_documents(docs)
    texts = [chunk.page_content for chunk in chunks]
    vector_store = FAISS.from_texts(texts, embeddings)
    return vector_store


# Load and index documents
docs = load_documents(documents)
vector_store = create_faiss_index(docs)

# Set up retriever
retriever = vector_store.as_retriever()

# If prompt is not empty, process the input
if prompt:
    response = ""
    if not search_internet:
        # Local LLM only
        llm = Ollama(model="llama3")
        context = retriever.get_relevant_documents(prompt)
        combined_context = " ".join([doc.page_content for doc in context])
        inputs = f"Context: {combined_context}\n\nQuestion: {prompt}\n\nAnswer:"
        response = llm.invoke(inputs)
    else:
        # LLM with internet search
        llm = Ollama(
            model="llama3",
            callback_manager=CallbackManager(
                [FinalStreamingStdOutCallbackHandler()])
        )
        agent = initialize_agent(
            load_tools(["ddg-search"]), llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, handle_parsing_errors=True
        )
        response = agent.run(prompt, callbacks=[
                             StreamlitCallbackHandler(st.container())])
        # To get out of a spiral Q&A: refresh the browser page

    # Display the response in Streamlit
    st.markdown(response)

# To run this script, save it as `app.py` and run the following command in your terminal:
# $ streamlit run app.py
