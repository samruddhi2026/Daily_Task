from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
import os
from pathlib import Path
from textwrap import dedent
from dotenv import load_dotenv


BASE_DIR = Path(__file__).parent
ROOT_DIR = BASE_DIR.parent

load_dotenv(ROOT_DIR / ".env")


def load_document(file_path):
    with open(BASE_DIR / file_path, "r", encoding="utf-8") as f:
        return f.read()


def split_text(text):
    lines = text.split("\n")
    chunks = []
    current = ""
    chunk_starts = ("\u25cf", "â—\u008f", "4.", "3.")

    for line in lines:
        if line.strip().startswith(chunk_starts):
            if current:
                chunks.append(current.strip())
            current = line
        else:
            current += " " + line

    if current:
        chunks.append(current.strip())

    return chunks


model = SentenceTransformer("all-MiniLM-L6-v2")

text = load_document("data.txt")
documents = split_text(text)

doc_embeddings = model.encode(documents)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment.")

genai.configure(api_key=api_key)
llm = genai.GenerativeModel("gemini-2.5-flash")


def retrieve(query):
    query_embedding = model.encode([query])
    scores = cosine_similarity(query_embedding, doc_embeddings)[0]
    index = scores.argmax()
    return documents[index]


def generate(context, query):
    prompt = dedent(
        f"""
        You are a helpful assistant.
        Use ONLY the provided context.
        If the answer is present, extract it directly and clearly.
        Do not add extra advice or invent details.
        If the answer is missing, reply exactly: Answer not found in context.

        Context:
        {context}

        Question:
        {query}

        Give a short, precise answer in plain text.
        """
    ).strip()
    response = llm.generate_content(
        prompt,
        generation_config={"temperature": 0.0},
    )
    return response.text.strip().strip("`")


def rag_pipeline(query):
    context = retrieve(query)
    answer = generate(context, query)
    return answer


def main():
    while True:
        q = input("User Query: ")
        if q == "exit":
            break
        print("Response:\n", rag_pipeline(q))


if __name__ == "__main__":
    main()
