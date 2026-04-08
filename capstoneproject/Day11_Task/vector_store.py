import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

with open("data.json") as f:
    data = json.load(f)

texts = [item["text"] for item in data]

embeddings = model.encode(texts)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))

faiss.write_index(index, "index.faiss")

with open("metadata.json", "w") as f:
    json.dump(data, f)

print("✅ Vector DB created successfully!")