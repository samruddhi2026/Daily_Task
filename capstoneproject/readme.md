# 👗 Urban-Edge Stylist

### AI-Powered Fashion Recommendation System using RAG & Semantic Vibe Mapping

---

## 📌 Project Overview

**Urban-Edge Stylist** is an AI-powered fashion recommendation system that suggests outfits based on a user’s desired *style vibe* (e.g., minimalist, edgy, streetwear).

The system combines:

* Semantic embeddings
* FAISS vector database
* Metadata tagging
* Agentic intent routing

to deliver intelligent, context-aware fashion recommendations.

---

## 🚀 Key Features

* 🔍 Semantic Search (embedding-based, not keyword-based)
* 🧠 Agentic Intent Routing
* 🗂️ Metadata Tagging (style, category, color)
* ⚡ FAISS Vector Database for fast retrieval
* 🛡️ Safety Layer for controlled responses
* 🎯 Multi-Prompt System for dynamic behavior

---

## 🧠 System Architecture

```text
User Query
   ↓
Safety Check
   ↓
Intent Router
   ↓
Query Embedding
   ↓
FAISS Vector Search
   ↓
Metadata Retrieval
   ↓
Response Generation
```

---

## 📂 Project Structure

```bash
capstoneproject/
│
├── Day10_Task/          # Benchmarking & evaluation
├── Day11_Task/          # Data engineering (Engine)
│   ├── data.json
│   ├── vector_store.py
│   ├── retriever.py
│   ├── index.faiss
│   ├── metadata.json
│
├── Day12_Task/          # Agentic logic (Brain)
│   ├── router.py
│   ├── prompts.py
│   ├── main.py
│
├── Day13_Task/          # Red-teaming & testing
├── Day14_Task/          # Performance optimization
│
└── README.md
```

---

## ⚙️ Technologies Used

* Python
* FAISS (Facebook AI Similarity Search)
* Sentence Transformers (`all-MiniLM-L6-v2`)
* NumPy
* JSON

---

## 🛠️ Installation & Setup

### 1. Clone Repository

```bash
git clone <your-repo-link>
cd capstoneproject
```

---

### 2. Create Virtual Environment (Optional)

```bash
python -m venv mlenv
mlenv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install faiss-cpu sentence-transformers numpy
```

---

### 4. Build Vector Database (Day 11)

```bash
python Day11_Task/vector_store.py
```

---

### 5. Run the System (Day 12)

```bash
python -m Day12_Task.main
```

---

## 🧪 Example Queries

### 🔹 Recommendation

```
minimalist outfit
```

### 🔹 Trend

```
latest fashion trends
```

### 🔹 General

```
hello
```

---

## 📊 Example Output

```
✨ Recommended Outfit:

1. Basic Black T-Shirt Minimal Wardrobe Essential
   → Style: minimalist

2. Black Oversized Hoodie Minimalist Streetwear
   → Style: minimalist

3. Minimalist Beige Hoodie Simple Design
   → Style: minimalist
```

---

## 🧠 How It Works

1. User query is analyzed using **Intent Router**
2. Query is converted into embeddings
3. FAISS retrieves semantically similar items
4. Metadata ensures structured output
5. Response is generated using prompt templates

---

## 📅 Project Progress

| Day    | Description                                     |
| ------ | ----------------------------------------------- |
| Day 10 | Benchmarking & tuning RAG system                |
| Day 11 | Data engineering (FAISS + metadata + retrieval) |
| Day 12 | Agentic logic (router + prompts + pipeline)     |
| Day 13 | Red-teaming & error resilience                  |
| Day 14 | Performance tuning & cost optimization          |

---

## 🛡️ Day 13 – Red-Teaming & Error Resilience

### Objective

To test system robustness against adversarial and invalid inputs.

### Tests Performed

* Bias testing across queries
* Adversarial prompts (instruction bypass attempts)
* Random/invalid inputs
* Safety-trigger inputs

### Example

```
hate fashion
```

Output:

```
Sorry, I cannot respond to that request.
```

### Outcome

* System remains stable
* No unsafe or hallucinated outputs
* Proper fallback responses

---

## ⚡ Day 14 – Performance Tuning & Optimization

### Objective

To improve system efficiency, speed, and scalability.

### Metrics

* Retrieval Time → Fast (FAISS optimized)
* Inference Time → Low latency
* Token Usage → Minimal (no large context passing)

### Improvements

* Reduced unnecessary processing
* Optimized top-k retrieval
* Simplified prompts

### Benchmark Results

| Query Type     | Result     |
| -------------- | ---------- |
| Recommendation | ✅ Accurate |
| Trend          | ✅ Correct  |
| General        | ✅ Handled  |
| Invalid Input  | ✅ Safe     |

---

## 🚀 Future Improvements

* Outfit combination logic (Top + Bottom + Shoes)
* Streamlit UI for better interaction
* User personalization
* Image-based recommendations
* Real-time trend integration

---

## 🎤 Interview Explanation

> I built an agentic RAG-based fashion recommendation system using FAISS and sentence-transformers. The system performs semantic retrieval based on user intent and uses an intent router with multi-prompting to dynamically generate responses. I also implemented red-teaming and performance optimization to ensure robustness and efficiency.

---

## 👩‍💻 Author

**Samruddhi Magdum**
AI & Data Science Enthusiast

---

## 📌 Conclusion

This project demonstrates how **AI + semantic search + agentic logic** can be combined to build scalable and intelligent recommendation systems.

---
