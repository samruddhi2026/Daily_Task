import faiss
import json
from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

BASE_DIR = os.path.dirname(__file__)
index_path = os.path.join(BASE_DIR, "index.faiss")
index = faiss.read_index(index_path)

metadata_path = os.path.join(BASE_DIR, "metadata.json")
with open(metadata_path) as f:
    metadata = json.load(f)

def retrieve(query, k=3):
    
    query_vec = model.encode([query])

    
    D, I = index.search(query_vec, k)

    results = []
    for idx in I[0]:
        results.append(metadata[idx])

    return results

