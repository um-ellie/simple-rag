from ollama import Client

from config import LLM_MODEL, OLLAMA_HOST, TOP_K
from retrieve import search


client = Client(host=OLLAMA_HOST)


SYSTEM_PROMPT = """You answer questions using ONLY the provided context.
If the context does not contain the answer, say you do not have enough information.
Do not use outside knowledge. Cite the context blocks you used as [1], [2], etc."""


def build_context(hits: list[dict]) -> str:
    return "\n\n".join(
        f"[{i}] (source: {hit['source']})\n{hit['text']}"
        for i, hit in enumerate(hits, start=1)
    )


def ask(question: str, context:str) -> str:
    response = client.chat(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n\n{context}\n\nQuestion: {question}"},
        ],
        think=False,
        options={"temperature": 0},
    )
    return response["message"]["content"]

def main() -> None:
    print("Ask a question (empty line to quit).")

    while True:
        question = input("\nQuestion: ").strip()
        if not question:
            break

        hits = search(question, k=TOP_K)
        context = build_context(hits)

        print("\n--- RETRIEVED CONTEXT ---\n")
        print(context)
        print("\n--- ANSWER ---\n")
        print(ask(question, context))


if __name__ == "__main__":
    main()