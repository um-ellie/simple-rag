from ollama import Client

from config import EMBEDDING_MODEL, OLLAMA_HOST

client = Client(host=OLLAMA_HOST)
BATCH_SIZE = 32


def embed_documents(texts: list[str]) -> list[list[float]]:
    vectors: list[list[float]] = []

    for i in range(0, len(texts), BATCH_SIZE):
        batch = [f"search_document: {t}" for t in texts[i : i + BATCH_SIZE]]
        response = client.embed(model=EMBEDDING_MODEL, input=batch)
        vectors.extend(response["embeddings"])

    return vectors


def embed_query(text: str) -> list[float]:
    response = client.embed(model=EMBEDDING_MODEL, input=f"search_query: {text}")

    return response["embeddings"][0]


if __name__ == "__main__":
    vector = embed_query("How do isolate python dependencies?")
    print("Dimensions:", len(vector))
    print("First values:", vector[:5])