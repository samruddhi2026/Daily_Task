# 👗 Urban-Edge Stylist

### AI-Powered Fashion Recommendation System using Semantic "Vibe" Mapping

---

## 📌 Project Overview

**Urban-Edge Stylist** is an AI-driven fashion recommendation system that suggests outfits based on a user's desired *style vibe* (e.g., minimalist, edgy, streetwear).

The system leverages:

* **Semantic embeddings**
* **Vector databases (FAISS)**
* **Metadata tagging**
* **Intent-based routing**

to provide intelligent, context-aware outfit recommendations.

---

## 🎯 Objective

To build a **Retrieval-Augmented Generation (RAG)** system that:

* Understands user intent
* Maps queries to fashion "vibes"
* Retrieves relevant items using vector similarity
* Generates meaningful outfit suggestions

---

## 🧠 Core Concept

Instead of keyword matching, this system uses **semantic similarity**:

* Converts fashion descriptions into embeddings
* Stores them in a vector database
* Matches user queries with similar embeddings

---

## ⚙️ System Architecture

```
User Query
   ↓
Safety Check
   ↓
Intent Router
   ↓
Query Embedding
   ↓
Vector Search (FAISS)
   ↓
Metadata Filtering
   ↓
Retrieved Fashion Items
   ↓
Response Generation
```

---

## 📂 Project Structure

```
capstoneproject/Day11_Task/
│
├── data.json              # Dataset with fashion items
├── vector_store.py       # Builds FAISS index
├── retriever.py          # Handles similarity search
├── router.py             # Intent classification
├── prompts.py            # Multi-prompt system
├── main.py               # Main execution pipeline
├── metadata.json         # Stored metadata
├── index.faiss           # Vector database
```

---

## 🗂️ Dataset Design

Each item contains:

* **text** → description for embedding
* **style_vibe** → semantic category
* **category** → clothing type
* **color** → optional attribute

### Example:

```json
{
  "text": "Black oversized hoodie minimalist streetwear",
  "style_vibe": "minimalist",
  "category": "topwear",
  "color": "black"
}
```

---

## 🔍 Key Features

### 1. Vector Database (FAISS)

* Stores embeddings of fashion items
* Enables fast similarity search

### 2. Metadata Tagging

* Adds structured filters like:

  * style_vibe
  * category
  * color

### 3. Parent Document Retrieval

* Retrieves full item details after vector match

### 4. Intent Routing

Classifies user queries into:

* Recommendation
* Trend Analysis
* General Query

### 5. Multi-Prompting

Different prompts for different intents:

* Styling
* Trends
* General advice

### 6. Safety Layer

Filters harmful or inappropriate queries

---

## 🔄 Workflow

### Step 1: User Input

Example:

```
"Suggest a minimalist outfit"
```

### Step 2: Intent Detection

→ Classified as `recommendation`

### Step 3: Embedding Generation

→ Query converted into vector

### Step 4: Vector Search

→ Similar items retrieved from FAISS

### Step 5: Metadata Mapping

→ Items filtered by style_vibe

### Step 6: Response Generation

### Output:

```
Recommended Outfit:
- Black oversized hoodie (minimalist)
- White sneakers (minimalist)
```

---

## 🧪 Example Queries

| Query               | Output                       |
| ------------------- | ---------------------------- |
| "Minimalist outfit" | Clean, simple clothing items |
| "Edgy street style" | Ripped jeans, leather jacket |
| "Sporty look"       | Track pants, running shoes   |

---

## 🛠️ Technologies Used

* **Python**
* **FAISS (Facebook AI Similarity Search)**
* **Sentence Transformers**
* **JSON (Data Storage)**

---

## 🚀 Implementation Highlights

### Embedding Model

```
all-MiniLM-L6-v2
```

### Vector Search

* L2 Distance similarity

### Retrieval Strategy

* Top-K nearest neighbors

---

## 📈 Future Improvements

* Outfit combination logic (Top + Bottom + Shoes)
* User personalization
* Real-time fashion trends integration
* Web UI using Streamlit
* Image-based recommendations

---

## 💼 Use Cases

* Personal styling assistants
* Fashion e-commerce platforms
* AI wardrobe planners
* Virtual fashion advisors

---

## 🎤 Interview Explanation (Short)

> I built a RAG-based fashion recommendation system that uses semantic embeddings and FAISS to retrieve outfit items based on user-defined style vibes. It includes metadata tagging, intent routing, and a modular prompt system for intelligent response generation.

---

## ✅ Conclusion

Urban-Edge Stylist demonstrates how **AI + semantic search** can enhance personalization in fashion. It combines data engineering, retrieval systems, and intelligent routing to create a scalable recommendation engine.

---
