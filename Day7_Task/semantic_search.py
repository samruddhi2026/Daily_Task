from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import warnings
from huggingface_hub import login
import os

warnings.filterwarnings("ignore")
load_dotenv()
hf_token = os.getenv("HF_TOKEN")
if hf_token:
    login(token=hf_token)

def load_corpus(file_name: str):
    corpus_path = Path(__file__).resolve().parent / file_name
    with corpus_path.open("r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]



model = SentenceTransformer("all-MiniLM-L6-v2")


sentences = load_corpus("corpus.txt")


sentence_embeddings = model.encode(sentences)


query = input("Enter your search query: ").strip()


if not query:
    print("Please enter a valid query.")
    exit()


query_embedding = model.encode([query])

similarities = cosine_similarity(query_embedding, sentence_embeddings)[0]


top_indices = similarities.argsort()[-3:][::-1]


threshold = 0.5

print("\nTop Results:\n")


if similarities[top_indices[0]] < threshold:
    print("No relevant results found in the file.")
else:
    for idx in top_indices:
        print(f"Score: {round(similarities[idx], 2)}")
        print(sentences[idx])
        print("----------------------")