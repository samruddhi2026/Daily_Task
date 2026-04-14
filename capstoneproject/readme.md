# 👗 Urban-Edge Stylist

### AI-Powered Fashion Recommendation System using RAG, Semantic Vibe Mapping & Gemini LLM

---

## 📌 Project Overview

**Urban-Edge Stylist** is a production-ready AI-powered fashion recommendation system that suggests outfits based on a user's desired *style vibe* (e.g., minimalist, edgy, streetwear).

The system combines:

* Semantic embeddings via sentence-transformers
* FAISS vector database for fast retrieval
* Metadata tagging (style, category, color)
* Agentic intent routing (recommendation, trend, general)
* Google Gemini LLM for intelligent response generation
* Safety layer for content validation
* Streamlit UI for end-user interaction
* Logging system for performance tracking

to deliver intelligent, context-aware fashion recommendations with LLM-enhanced responses.

---

## 🚀 Key Features

* 🔍 **Semantic Search** - Embedding-based retrieval, not keyword matching
* 🧠 **Agentic Intent Routing** - Classifies queries to recommendation, trend, or general categories
* 🗂️ **Metadata Tagging** - Enriches results with style, category, and color information
* ⚡ **FAISS Vector Database** - Ultra-fast similarity search
* 🛡️ **Safety Layer** - Blocks hate speech, offensive, abuse, and illegal content
* 🎯 **Multi-Prompt System** - Dynamic prompts based on intent
* 🤖 **Gemini LLM Integration** - Generates polished, contextual responses
* 🎨 **Streamlit UI** - Beautiful wardrobe-themed interface with outfit display
* 📊 **Performance Logging** - Tracks query, processing time, and results

---

## 🧠 System Architecture

```text
User Query (Streamlit UI)
   ↓
Safety Check (Input Validation)
   ↓
Intent Router (Recommendation/Trend/General)
   ↓
Query Embedding (Sentence-Transformers)
   ↓
FAISS Vector Search (Fast Retrieval)
   ↓
Metadata Enrichment (Style, Category, Color)
   ↓
Gemini LLM Processing (Response Generation)
   ↓
Output Formatting & Logging
   ↓
Streamlit Display (Outfit Rack)
```

---

## 📂 Project Structure

```bash
capstoneproject/
│
├── Day11_Task/              # Data Engineering (Vectorization)
│   ├── __init__.py
│   ├── data.json            # Fashion dataset
│   ├── vector_store.py      # Creates FAISS index
│   ├── retriever.py         # Retrieval logic
│   ├── index.faiss          # Pre-built FAISS index
│   └── metadata.json        # Style metadata
│
├── Day12_Task/              # Agentic Logic & Gemini Integration
│   ├── __init__.py
│   ├── main.py              # Core pipeline with Gemini API
│   ├── router.py            # Intent routing
│   └── prompts.py           # Multi-prompt templates
│
├── Day13_Task/              # Red-Teaming & Testing
│   └── test_redteam.py      # Adversarial input handling
│
├── Day14_Task/              # Performance Optimization
│   └── performance_test.py  # Benchmarking
│
├── Day15_Task/              # Streamlit Frontend & Logging
│   ├── __init__.py
│   ├── app.py               # Streamlit wardrobe UI
│   └── log.txt              # Runtime logs
│
│
├── .env                     # Environment variables (parent folder)
├── readme.md                # This file
└── Urban-Edge-Stylist.pptx  # Final presentation

Key Files:
- D:\Daily_Task\.env        # Contains GEMINI_API_KEY
```

---

## ⚙️ Technologies Used

* **Python** - Core language
* **FAISS** - Vector similarity search (Facebook AI)
* **Sentence-Transformers** - Embedding model (`all-MiniLM-L6-v2`)
* **Google Gemini API** - LLM for text generation
* **NumPy** - Numerical computing
* **JSON** - Data storage & metadata
* **Streamlit** - Web UI framework
* **Requests** - HTTP library for Gemini API calls
* **dotenv** - Environment variable management

---

## 🛠️ Installation & Setup

### 1. Clone Repository

```bash
git clone <your-repo-link>
cd capstoneproject
```

### 2. Create Virtual Environment

```bash
python -m venv mlenv
mlenv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install faiss-cpu sentence-transformers numpy streamlit requests python-dotenv torchvision
```

### 4. Configure API Key

The project reads `GEMINI_API_KEY` from `D:\Daily_Task\.env`:


The key is **automatically loaded** by `Day12_Task/main.py` when generating responses.

### 5. Build Vector Database (Optional - Pre-built included)

```bash
python Day11_Task/vector_store.py
```

### 6. Run Streamlit UI

```bash
cd Day15_Task
streamlit run app.py
```

Access at: `http://localhost:8501`

---

## 🧪 Example Usage

### Terminal Usage

```bash
python Day12_Task/main.py
# Enter query: minimalist outfit
```

### Streamlit Usage

1. Open `http://localhost:8501`
2. Enter style vibe (e.g., "edgy streetwear")
3. Click "✨ Get Recommendation"
4. View outfit suggestions in display window

### Example Queries

| Query                    | Intent         | Response Type         |
| ------------------------ | -------------- | --------------------- |
| minimalist outfit        | recommendation | FAISS retrieval + LLM |
| latest fashion trends    | trend          | Gemini generation     |
| what should i wear today | general        | Gemini response       |
| hate fashion             | (blocked)      | Safety filter blocked |

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

[Gemini LLM Enhanced Response]
These pieces combine simplicity with functionality, perfect for a minimalist 
wardrobe. The neutral color palette ensures versatility and timeless appeal.
```

---

## 🧠 How It Works

### Core Pipeline

1. **User Input**: Query entered via Streamlit or terminal
2. **Safety Check**: Validates input against banned keywords (hate, offensive, abuse, illegal)
3. **Intent Routing**: Router classifies intent as:
   - `recommendation` → FAISS retrieval
   - `trend` → Gemini generation
   - `general` → Gemini generation
4. **Embedding**: Query converted to embeddings using sentence-transformers
5. **Retrieval**: FAISS searches top-5 similar fashion items
6. **Metadata Enrichment**: Attaches style, category, color tags
7. **LLM Processing**: Gemini API polishes response (if enabled)
8. **Formatting**: Output structured and logged
9. **Display**: Results shown in Streamlit wardrobe interface

### Gemini API Integration

- **Endpoint**: `https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText`
- **Auth**: API key in `GEMINI_API_KEY` environment variable
- **Temperature**: 0.7 (balanced creativity)
- **Max Tokens**: 300 (concise responses)

---

## 📅 Project Timeline

| Phase  | Description                                          | Status |
| ------ | ---------------------------------------------------- | ------ |
| Day 11 | Data engineering, FAISS index, metadata handling     | ✅     |
| Day 12 | Intent router, prompts, Gemini integration           | ✅     |
| Day 13 | Red-teaming, adversarial input handling              | ✅     |
| Day 14 | Performance optimization, benchmarking               | ✅     |
| Day 15 | Streamlit UI, logging system, final polish           | ✅     |

---

## 🛡️ Safety & Validation

### Input Filtering

Banned keywords: `hate`, `offensive`, `abuse`, `illegal`

### Query Validation

- Minimum length: 3 characters
- Max safety violations: Auto-rejected
- Empty queries: Warned with message

### Output Normalization

- Consistent formatting
- Metadata validation
- Response truncation (300 tokens max)

---

## ⚡ Performance Metrics

### Benchmarked Results

- **Retrieval Time**: ~0.4 sec (FAISS optimized)
- **Gemini Response Time**: ~1.0 sec (API-dependent)
- **Total Query Time**: ~1.5 sec average
- **Throughput**: 40+ queries/minute

### Logging System

```
Query: minimalist outfit
Task: retrieval
Processing Time: 0.42 sec
Output Preview: Basic Black T-Shirt, Black Oversized Hoodie, Minimalist Beige Hoodie
Notes: Successful recommendation
```

Logs stored in: `Day15_Task/log.txt`

---

## 🧪 Testing & Validation

### Red-Team Test Cases

| Test Category | Example Input            | Expected Behavior        |
| ------------- | ------------------------ | ------------------------ |
| Normal        | minimalist outfit        | ✅ Recommendations      |
| Safety        | hate fashion             | ✅ Blocked               |
| Edge case     | (empty query)            | ✅ Warning message       |
| Noise         | 12345 asdfg              | ✅ Handled gracefully    |
| Long query    | [very long text...]      | ✅ Processed             |

### Performance Tests

Run benchmarking:

```bash
python Day14_Task/performance_test.py
```

---

## 🎨 Streamlit UI Features

### Wardrobe Theme

- **Sidebar**: "Stylist's Closet" with example vibes
- **Banner**: Brand title and description
- **Input Field**: Style vibe text box
- **Button**: "✨ Get Recommendation"
- **Display**: Two-column outfit cards with:
  - Item name
  - Style tag
  - Metadata badge
  - Mannequin-style layout

### Outfit Card Design

```
┌─────────────────────────────────┐
│ 1. Edgy Ripped Jacket          │
│                                 │
│ Style: edgy                    │
│ ┌──────────────────────────┐   │
│ │   Mannequin Style        │   │
│ └──────────────────────────┘   │
└─────────────────────────────────┘
```

---

## 🚀 Future Enhancements

* 🖼️ Image-based recommendations (CV model integration)
* 👤 User personalization & preference learning
* 👕 Outfit combination logic (full OOTD generation)
* 🌍 Real-time trend scraping
* 💬 Chat-based interface
* 📱 Mobile app version
* 🎯 A/B testing framework

---

## 📝 How to Run Everything

### Quick Start

```bash
# 1. Activate environment
mlenv\Scripts\activate

# 2. Run Streamlit app
cd Day15_Task
streamlit run app.py

# 3. Open http://localhost:8501
```

### Full System Test

```bash
# Terminal 1: Streamlit UI
streamlit run Day15_Task/app.py

# Terminal 2: Performance test (optional)
python Day14_Task/performance_test.py

# Terminal 3: Direct Python usage
python Day12_Task/main.py
```

---

## 🎓 Key Learnings

* **Semantic Search > Keyword Matching** - Embeddings capture intent better
* **Agentic Routing** - Intent classification enables flexible response generation
* **LLM Augmentation** - Gemini polish makes outputs more natural and personalized
* **Safety First** - Validation prevents abuse and maintains system integrity
* **Logging Matters** - Tracking metrics enables debugging and optimization
* **UI/UX Polish** - Streamlit makes the system accessible to non-technical users

---

## 🎤 Project Summary

> Urban-Edge Stylist is a full-stack AI fashion recommendation system combining:
> - Semantic vector search (FAISS + embeddings)
> - Intelligent intent routing
> - LLM-enhanced response generation (Gemini)
> - Robust safety validation
> - Beautiful Streamlit interface
> 
> Demonstrates real-world RAG pipeline, agentic AI, API integration, and production-grade design.

---

## 👩‍💻 Author

**Samruddhi Magdum**  
AI & Data Science Enthusiast  
Capstone Project: Urban-Edge Stylist  
Date: April 14, 2026

---

## 📞 Contact & Support

For issues or questions:
1. Check `Day15_Task/log.txt` for runtime errors
2. Verify `.env` file has `GEMINI_API_KEY`
3. Ensure all dependencies installed: `pip install -r requirements.txt`
4. Review test cases in `Day13_Task/test_redteam.py`

---

## 📌 Conclusion

**Urban-Edge Stylist** demonstrates how **semantic search + agentic logic + LLM integration** can be combined to build scalable, intelligent, and user-friendly recommendation systems. It reflects best practices in RAG architecture, API integration, safety validation, and modern UI/UX design.

---

**Status**: ✅ Project Complete & Ready for Submission

**Next Steps**: Present PPT, demonstrate live UI, explain architecture to stakeholders.
