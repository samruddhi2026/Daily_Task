import faiss
import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')


index = faiss.read_index("index.faiss")


with open("metadata.json") as f:
    metadata = json.load(f)

def retrieve(query, k=3):
    
    query_vec = model.encode([query])

    
    D, I = index.search(query_vec, k)

    results = []
    for idx in I[0]:
        results.append(metadata[idx])

    return results



if __name__ == "__main__":
    query = "minimalist outfit"
    results = retrieve(query)

    for item in results:
        print(item)