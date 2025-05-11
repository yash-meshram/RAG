import streamlit as st 
from pdfLoader import PDFLoader
from vectorStore import VectorStore
from chain import Chain
import asyncio

st.title("Retrieval-augmented generation (RAG)")

question = st.text_input(
    "Ask question related to the document",
    value = "what is decision tree?"
)

submit = st.button("Submit")

def get_response(question):
    # Uncomment the below 2 steps if - 1. you are running the code for the first time 2. want to add the another document data in vector store
    
    # Loading all the pdfs in data directory
    document_pages = asyncio.run(
        PDFLoader.load_all_pdfs_from_directory(
            data_directory = "app/data/Documents"
        )
    )
    
    # creating the vector store
    VectorStore.create_vector_store(document_pages)

    # search question in vector store
    pages_data = VectorStore.search(question = question)

    # getting the answer
    chain = Chain()
    answer = chain.get_answer(question = question, docs_data = pages_data)
    return answer

if submit:
    answer = get_response(question)
    st.markdown(answer)
