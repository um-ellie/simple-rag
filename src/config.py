from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = ROOT / "notes"
CHROMA_DIR = ROOT / "data" / "chroma"

OLLAMA_HOST = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "qwen3.5:4b"

COLLECTION_NAME = "notes"

MAX_CHUNK_CHARS = 800   # Maximum number of characters in each chunk
CHUNK_OVERLAP_CHARS = 100  # Number of characters to overlap between chunks
TOP_K = 4  # Number of top results to return