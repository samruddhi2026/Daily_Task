import os
import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pathlib import Path
from google import genai


def load_document():
    path = Path(__file__).parent / "document.txt"
    with path.open("r", encoding="utf-8") as f:
        return f.read()

def split_text(text, chunk_size=100):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

def store_chunks(chunks, model):
    db_path = Path(__file__).parent / "chroma_db"
    client = chromadb.PersistentClient(path=str(db_path))

    try:
        client.delete_collection("rag_collection")
    except Exception:
        pass

    collection = client.create_collection("rag_collection")

    embeddings = model.encode(chunks).tolist()
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(ids=ids, documents=chunks, embeddings=embeddings)
    return collection


def retrieve(query, collection, model):
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3  
    )

    context = " ".join(results["documents"][0])
    return context, query_embedding[0]


def generate_answer(question, context):
    prompt = f"""
Answer the question using ONLY the provided context.
If the answer is not in the context, say I DON'T KNOW.

Context:
{context}

Question:
{question}
"""

    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        try:
            client = genai.Client(api_key=api_key)

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt
            )

            return response.text.strip()

        except Exception as e:
            print("Gemini error:", e)

    question_words = question.lower().split()
    context_lower = context.lower()

    for word in question_words:
        if len(word) > 3 and word in context_lower:
            sentences = context.split(".")
            if len(sentences) > 0 and sentences[0].strip():
                return sentences[0].strip() + "."
            return context

    return "I DON'T KNOW."


def print_query_debug(question, query_embedding):
    print(f"Query: {question}\n")
    print("Query Embedding:")
    print(query_embedding)


def main():
    load_dotenv()

    print("Starting RAG system...")

    try:
        text = load_document()
    except FileNotFoundError:
        print("document.txt not found.")
        return

    if not text.strip():
        print("document.txt is empty.")
        return

    print("Document loaded")

    
    chunks = split_text(text)
    print("Chunks created:", len(chunks))

    
    model = SentenceTransformer("all-MiniLM-L6-v2")

   
    collection = store_chunks(chunks, model)

    if os.getenv("GEMINI_API_KEY"):
        print("Gemini API key found")
    else:
        print("No Gemini API key found, fallback mode")

    print("RAG system ready; type 'exit' to stop")

    
    while True:
        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            break

        if not question:
            print("Please ask something")
            continue

        
        context, query_embedding = retrieve(question, collection, model)
        answer = generate_answer(question, context)

        print("\nAnswer:")
        print(answer)
        print()
        print_query_debug(question, query_embedding)



if __name__ == "__main__":
    main()
