import chromadb

from config import CHROMA_DIR, COLLECTION_NAME

_client = chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_collection():
    return _client.get_or_create_collection(
        name=COLLECTION_NAME,
        configuration={"hnsw": {"space": "cosine"}}
    )