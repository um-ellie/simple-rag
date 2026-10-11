import hashlib

from chunker import chunk_markdown
from config import NOTES_DIR
from database import get_collection
from embeddings import embed_documents


def file_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stored_hashes(collection) -> dict[str, str]:

    metadatas = collection.get(include=["metadatas"])["metadatas"]
    return {m["source"]: m["file_hash"] for m in metadatas}


def ingest() -> None:
    collection = get_collection()
    known = stored_hashes(collection)
    seen: set[str] = set()
    added = updated = skipped = removed = 0

    for path in sorted(NOTES_DIR.rglob("*.md")):
        source = path.relative_to(NOTES_DIR).as_posix()
        seen.add(source)

        text = path.read_text(encoding="utf-8")
        digest = file_hash(text)

        if known.get(source) == digest:
            skipped +=1
            continue

        chunks = chunk_markdown(text)
        vectors = embed_documents([c.text for c in chunks]) if chunks else []

        if source in known:
            collection.delete(where={"source": source})
            updated += 1
        else:
            added += 1

        if chunks:
            collection.add(
                ids=[f"{source}::{c.index}" for c in chunks],
                documents=[c.text for c in chunks],
                embeddings=vectors,
                metadatas=[
                    {
                        "source": source,
                        "heading": c.heading,
                        "chunk_index": c.index,
                        "file_hash": digest,
                    }
                    for c in chunks
                ],
            )

    for source in set(known) - seen:
        collection.delete(where={"source": source})
        removed += 1

    print(
        f"Files: {added} added, {updated} updated, {skipped} unchanged, {removed} removed, "
        f"Total chunks: {collection.count()}"
    )


if __name__ == "__main__":
    ingest()