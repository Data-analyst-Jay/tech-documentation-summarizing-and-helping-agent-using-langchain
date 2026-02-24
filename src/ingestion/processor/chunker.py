# processor/chunking.py

from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(documents: List[Document]) -> List[Document]:
    """
    Splits documents into smaller chunks using RecursiveCharacterTextSplitter.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=[
            "\n## ",    #preserving H2 section
            "\n### ",   #presering H3 section
            "\n\n", 
            "\n", 
            " ", 
            ""],
    )

    chunked_docs = text_splitter.split_documents(documents)

    return chunked_docs
