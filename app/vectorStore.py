from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import pickle

class VectorStore:
    # Creating the vector store
    def create_vector_store(pages: list):
        embedding = HuggingFaceEmbeddings(
            model_name = "sentence-transformers/all-mpnet-base-v2"
        )
        vector_store = InMemoryVectorStore.from_documents(
            pages, embedding
        )
        with open("data/VectorStore/vector_store.pkl", "wb") as f:
            pickle.dump(vector_store, f)
        
    # Searching in the created vectore store
    def search(question: str) -> list:
        with open("data/VectorStore/vector_store.pkl", "rb") as f:
            vector_store = pickle.load(f)
        pages = vector_store.similarity_search(
            query = question,
            k = 3
        )
        pages_data = []
        for page in pages:
            dict_ = {
                "doc_title": page.metadata['title'].strip(),
                "page_no": page.metadata['page_label'].strip(),
                "page_content": page.page_content.strip()
            }
            pages_data.append(dict_)
        return pages_data
    
# if __name__ == "__main__":
#     pages_data = VectorStore.search("What is decision tree?")
#     print(pages_data)