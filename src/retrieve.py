from database import get_collection
from embeddings import embed_query


def search(query: str, k: int = 4, max_distance: float | None = None) -> list[dict]:
    collection = get_collection()
    count = collection.count()

    if count == 0:
        raise SystemExit("The database is empty. Run: uv run python src/ingest.py")

    results = collection.query(
        query_embeddings=[embed_query(query)],
        n_results=min(k, count),
        include=["documents", "metadatas", "distances"],
    )

    hits = [
        {
            "text": document,
            "source": metadata["source"],
            "heading": metadata["heading"],
            "distance": distance,
        }
        for document, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]

    if max_distance is not None:
        hits = [h for h in hits if h["distance"] <= max_distance]
    return hits


if __name__ == "__main__":
    query = input("Ask a Question: ")
    for i, hit in enumerate(search(query), start=1):
        print(f"\n--- RESULT {i} | {hit['source']} | {hit['heading']} | Distance {hit['distance']:.3f} ---")
        print(hit["text"])