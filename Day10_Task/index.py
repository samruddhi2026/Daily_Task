from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from google import genai
from pathlib import Path
import os

def load_document(file_path):
    path = Path(file_path)
    if not path.is_absolute():
        path = Path(__file__).resolve().parent / path
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
client = genai.Client(api_key=API_KEY) if API_KEY else None

def semantic_chunking(text):
    prompt = f"""
    Split the following text into meaningful chunks.
    Each chunk should contain a complete idea or topic.
    Do not break sentences randomly.

    Text:
    {text}

    Return chunks separated by ###.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    chunks = response.text.split("###")
    return [c.strip() for c in chunks if len(c.strip()) > 50]

model = SentenceTransformer("all-MiniLM-L6-v2")

text = load_document("data.txt")

def answer_from_context(query, context):
    prompt = f"""
You are an expert AI system evaluating technical queries.

Answer the question ONLY using the provided context.

Rules:
- Do NOT add any external knowledge
- Do NOT hallucinate
- Extract the most relevant information from the context
- If the answer exists, return it clearly and concisely
- If partially available, return the closest correct information
- Only say "Not found in context" if absolutely no relevant info exists

Context:
{context}

Question:
{query}

Give a short, precise, and complete answer.
"""
    if client is None:
        return context

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception:
        return context

def chunk_by_words(source_text, chunk_size):
    words = source_text.split()
    chunks = []
    current = []
    current_len = 0

    for w in words:
        # +1 for the joining space when needed.
        add_len = len(w) if current_len == 0 else len(w) + 1
        if current and current_len + add_len > chunk_size:
            chunks.append(" ".join(current))
            current = [w]
            current_len = len(w)
        else:
            current.append(w)
            current_len += add_len

    if current:
        chunks.append(" ".join(current))

    return chunks

def build_system(chunk_size=200):
    documents = chunk_by_words(text, chunk_size)

    embeddings = model.encode(documents)
    return documents, embeddings

def retrieve(query, documents, embeddings, top_k=2):
    query_embedding = model.encode([query])
    scores = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = scores.argsort()[-top_k:][::-1]
    return "\n\n".join(documents[i] for i in top_indices)

def read_score():
    while True:
        raw = input("Enter groundedness score (1-5): ").strip()
        try:
            value = int(raw)
            if 1 <= value <= 5:
                return value
        except ValueError:
            pass
        print("Invalid score. Please enter a number from 1 to 5.")

def evaluate_configuration(config_name, chunk_size, questions):
    documents, embeddings = build_system(chunk_size=chunk_size)
    print(f"\n=== {config_name} (chunk_size={chunk_size}) ===")

    scores = []

    for q in questions:
        print("\nQuestion:", q)
        context = retrieve(q, documents, embeddings, top_k=2)
        answer = answer_from_context(q, context)
        print("Answer:", answer)
        score = read_score()
        scores.append(score)

    avg_score = sum(scores) / len(scores)
    return avg_score

QUESTIONS = [
    "I'm seeing Error XV-505 in my terminal. What is the root cause and how do I fix it?",
    "My system is extremely laggy. Which shards should I be worried about and what is the specific command to reset them?",
    "Can I bypass the Theta-Sync requirement to install this on my old i7 laptop?",
    "How does the OS handle user login now that passwords and 2FA are deprecated?",
    "I have a MAC address that was black-holed by the Wraith Firewall. Can I unblock it using the Galactic-Relay?"
]

baseline_score = evaluate_configuration("Before (Baseline)", 200, QUESTIONS)
tuned_score = evaluate_configuration("After (Tuned)", 600, QUESTIONS)

print("\nBenchmark Results")
print(f"{'Configuration':<22} {'Chunk Size':<10} {'Avg Groundedness':<16}")
print("-" * 52)
print(f"{'Before (Baseline)':<22} {200:<10} {baseline_score:<16.2f}")
print(f"{'After (Tuned)':<22} {600:<10} {tuned_score:<16.2f}")

if tuned_score > baseline_score:
    print("\nWinner: After (Tuned)")
elif tuned_score < baseline_score:
    print("\nWinner: Before (Baseline)")
else:
    print("\nWinner: Tie")
