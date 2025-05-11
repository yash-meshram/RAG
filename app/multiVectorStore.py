from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import pickle
import os
from typing import Dict, List

class MultiVectorStore:
    def __init__(self):
        self.vector_stores: Dict[str, InMemoryVectorStore] = {}
        self.embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        self.vector_store_dir = "app/data/vector_stores"
        # Create directory if it doesn't exist
        os.makedirs(self.vector_store_dir, exist_ok=True)

    def create_vector_store(self, pages: List, doc_name: str):
        """
        Create a vector store for a specific document
        
        Args:
            pages: List of document pages
            doc_name: Name of the document (will be used as identifier)
        """
        # Create vector store for the document
        vector_store = InMemoryVectorStore.from_documents(
            pages, self.embedding
        )
        
        # Save the vector store
        store_path = os.path.join(self.vector_store_dir, f"{doc_name}_vector_store.pkl")
        with open(store_path, "wb") as f:
            pickle.dump(vector_store, f)
        
        # Store in memory
        self.vector_stores[doc_name] = vector_store

    def load_vector_store(self, doc_name: str) -> InMemoryVectorStore:
        """
        Load a specific vector store from disk
        
        Args:
            doc_name: Name of the document
        """
        store_path = os.path.join(self.vector_store_dir, f"{doc_name}_vector_store.pkl")
        if os.path.exists(store_path):
            with open(store_path, "rb") as f:
                vector_store = pickle.load(f)
            self.vector_stores[doc_name] = vector_store
            return vector_store
        return None

    def search_in_document(self, question: str, doc_name: str, k: int = 3) -> List[dict]:
        """
        Search for answers in a specific document
        
        Args:
            question: The question to search for
            doc_name: Name of the document to search in
            k: Number of results to return
        """
        # Load vector store if not in memory
        if doc_name not in self.vector_stores:
            vector_store = self.load_vector_store(doc_name)
            if vector_store is None:
                return []

        pages = self.vector_stores[doc_name].similarity_search(
            query=question,
            k=k
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

    def search_all_documents(self, question: str, k: int = 3) -> List[dict]:
        """
        Search for answers across all documents
        
        Args:
            question: The question to search for
            k: Number of results to return per document
        """
        all_results = []
        
        # Get all vector store files
        vector_store_files = [f for f in os.listdir(self.vector_store_dir) 
                            if f.endswith("_vector_store.pkl")]
        
        for store_file in vector_store_files:
            doc_name = store_file.replace("_vector_store.pkl", "")
            results = self.search_in_document(question, doc_name, k)
            all_results.extend(results)
        
        # Sort results by relevance (you might want to implement a more sophisticated
        # ranking system here)
        return all_results

    def get_available_documents(self) -> List[str]:
        """
        Get list of all available documents
        """
        vector_store_files = [f for f in os.listdir(self.vector_store_dir) 
                            if f.endswith("_vector_store.pkl")]
        return [f.replace("_vector_store.pkl", "") for f in vector_store_files]

    def delete_vector_store(self, doc_name: str):
        """
        Delete a specific vector store
        
        Args:
            doc_name: Name of the document to delete
        """
        store_path = os.path.join(self.vector_store_dir, f"{doc_name}_vector_store.pkl")
        if os.path.exists(store_path):
            os.remove(store_path)
            if doc_name in self.vector_stores:
                del self.vector_stores[doc_name] 