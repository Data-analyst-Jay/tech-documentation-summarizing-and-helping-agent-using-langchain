from langchain_community.embeddings import OllamaEmbeddings

def get_emembedding_model():
    """
    Returns Ollama embedding model using nomic-embed-text.
    """
    return OllamaEmbeddings(
        model="nomic-embed-text:latest"
    )