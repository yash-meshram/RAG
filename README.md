# RAG PDF QA

Retrieval-Augmented Generation (RAG) is a Streamlit-based application that allows users to ask questions about the content of PDF documents. It leverages vector stores and large language models to provide accurate, reference-backed answers based on the provided documents.

## Features
- **PDF Document Ingestion:** Load and process PDF files from a specified directory.
- **Vector Store Creation:** Embed and store document pages for efficient semantic search.
- **Question Answering:** Ask questions about the ingested documents and receive answers with references to the source document and page.
- **Streamlit UI:** Simple web interface for user interaction.


## Directory Structure
```
├── app/
│   ├── main.py                # Streamlit app entry point
│   ├── pdfLoader.py           # PDF loading utilities
│   ├── vectorStore.py         # Single vector store management
│   ├── multiVectorStore.py    # Multi-document vector store management ("ongoing")
│   ├── chain.py               # LLM chain and prompt logic
├── data/
│   ├── Documents/             # Place your PDF files here
│   │   └── document.txt       # Directory guide ("Put the pdf file in this directory.")
│   └── VectorStore/           # Stores vector store pickle files
│       ├── vector_store.pkl   # Main vector store file
│       └── vector_store.txt   # Directory guide ("Vector store will be created in this directory.")
├── README.md                  # Project documentation
```

## Diagram

<picture>
  <source srcset="data/Diagram/diagram-dark.png" media="(prefers-color-scheme: dark)">
  <source srcset="data/Diagram/diagram-light.png" media="(prefers-color-scheme: light)">
  <img src="app/resources/diagram-light.png" alt="Project Workflow">
</picture>

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd <repo-directory>
   ```
2. **Install dependencies:**
   Create a `requirements.txt` with the following (or use your preferred environment manager):
   ```
   streamlit
   langchain
   langchain-community
   langchain-huggingface
   langchain-groq
   python-dotenv
   sentence-transformers
   ```
   Then install:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   - Create a `.env` file in the root or `app/` directory with your [Groq API key](https://console.groq.com/):
     ```
     GROQ_API_KEY=your_groq_api_key_here
     ```
4. **Add PDF documents:**
   - Place your PDF files in `data/Documents/`.

## Usage
1. **Run the Streamlit app:**
   ```bash
   streamlit run app/main.py
   ```
2. **Interact via the web UI:**
   - Enter your question in the input box and click "Submit".
   - The app will search the ingested documents and return an answer with references.

**Note:**
- On first run or when adding new documents, the app will process all PDFs and create/update the vector store. This may take some time depending on the number and size of documents.
- The `data/Documents/document.txt` and `data/VectorStore/vector_store.txt` files are directory guides and can be safely ignored or removed if not needed.

## Enhancement

**In Progress**
- Implementation of robust support for managing and querying multiple PDF documents simultaneously.

**Planned Enhancements**
- Enable users to upload their own PDF files directly through the web interface.
- Extend document processing capabilities to support a wider range of file formats beyond PDFs.

## Dependencies
- [Streamlit](https://streamlit.io/)
- [LangChain](https://python.langchain.com/)
- [sentence-transformers](https://www.sbert.net/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [Groq LLM API](https://console.groq.com/)

## Environment Variables
- `GROQ_API_KEY`: Your API key for Groq LLM access (required).

## License
Specify your license here.

## Acknowledgements
- Built with [LangChain](https://python.langchain.com/) and [Streamlit](https://streamlit.io/).