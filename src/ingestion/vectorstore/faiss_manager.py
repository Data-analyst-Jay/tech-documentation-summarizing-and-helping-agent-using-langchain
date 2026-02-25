import os
from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

def create_faiss_index(documents: List[Document], embedding_model):
    '''
    Creates a FAISS index from documents.
    '''
    if not documents:
        raise ValueError("No documents provided for indexing.")
    
    vector_store = FAISS.from_documents(
        documents,
        embedding_model
    )

    return vector_store

def save_faiss_index(vector_store, index_path: str):
    '''
    Saves the FAISS index locally.'''

    os.makedirs(index_path, exist_ok=True)
    vector_store.save_local(index_path)

def load_faiss_index(index_path: str, embedding_model):
    '''
    Loads FAISS index from the disk.
    '''

    return FAISS.load_local(
        index_path,
        embedding_model,
        allow_dangerous_deserialization=True
    )