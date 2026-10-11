from config import TOP_K
from retrieve import search


CASES = [
    ("How do I isolate Python dependencies?", "python.md"),
    ("How do I keep packages of different projects separate?", "python.md"),
    ("How do I see running processes?", "linux.md"),
    ("What does DNS do?", "networking.md"),
    ("How many bits are in an IPv4 address?", "networking.md"),
    ("What is the difference between authentication and authorization?", "security.md"),
    ("How should I store passwords?", "security.md"),
]


def main() -> None:
    hits_at_1 = hits_at_k = 0
    for question, expected in CASES:
        sources = [h["source"] for h in search(question, k=TOP_K)]
        top_1 = sources[0] == expected
        in_k = expected in sources
        hits_at_1 += top_1
        hits_at_k += in_k
        status = "OK " if top_1 else ("TOP-K" if in_k else "MISS")
        print(f"{status}   {question}  ->  {sources}")


    n = len(CASES)
    print(f"\nTop-1: {hits_at_1}/{n}    Top-{TOP_K}:  {hits_at_k}/{n}")


if __name__ == "__main__":
    main()