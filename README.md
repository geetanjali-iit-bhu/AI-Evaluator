# ExamForge — AI Question Paper Generator

An AI-powered question paper generator that uses **Retrieval-Augmented Generation (RAG)** to create structured, IIT-style examination papers directly from a professor's own course material.

---

## What it does

A professor uploads their PDFs, PPTs or DOCX notes — and the system automatically generates a fully structured question paper with:
- Multiple Choice Questions (with options + correct answers)
- Short Answer Questions (with per-question marking scheme)
- Long Answer / Essay Questions (with detailed marks breakdown)

Questions are generated **strictly from the uploaded material** — not from general internet knowledge.

---

## How it works

```
Professor's Notes (PDF/PPTX/DOCX)
        ↓
   Text Extraction & Chunking
        ↓
   FAISS Vector Index (stored on disk)
        ↓
   Topic Query → Semantic Retrieval (top-8 chunks)
        ↓
   Prompt Engineering (difficulty + rubric + context)
        ↓
   LLaMA 3.3 70B via Groq API
        ↓
   Structured Question Paper → ExamForge UI
```

---

## Tech Stack

| Component | Technology |
|---|---|
| Embedding Model | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector Database | FAISS |
| LLM | LLaMA 3.3 70B via Groq API |
| RAG Framework | LangChain |
| Backend API | Flask |
| Frontend | Vanilla HTML/CSS/JS (ExamForge UI) |
| Document Parsing | pdfplumber, python-pptx, python-docx |

---

## Project Structure

```
AI-Evaluator/
├── api.py              # Flask API — connects UI to RAG pipeline
├── rag_pipeline.py     # Core RAG logic — retrieval + prompt + LLM call
├── vector_store.py     # Builds and loads FAISS index
├── ingestion.py        # Loads and chunks PDF/PPTX/DOCX/TXT files
├── evaluation.py       # (WIP) Student answer evaluation
├── main.py             # CLI entry point
├── examforge.html      # Frontend UI
├── requirements.txt    # Python dependencies
├── data/               # ← Put your notes/PDFs here (not pushed to git)
├── faiss_index/        # ← Auto-generated after running vector_store.py
└── .env                # ← Your API keys (not pushed to git)
```

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/geetanjali-iit-bhu/AI-Evaluator.git
cd AI-Evaluator
```

### 2. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get a free API key at [console.groq.com](https://console.groq.com)

### 5. Add your course material
Create a `data/` folder and drop in your files:
```bash
mkdir data
# Add your PDFs, PPTs, DOCX files into data/
```
Supported formats: `.pdf`, `.pptx`, `.docx`, `.txt`

### 6. Build the vector index
```bash
python vector_store.py
```
This reads all files from `data/`, chunks them, embeds them and saves the FAISS index. Run this again whenever you add new files.

### 7. Start the app
```bash
python api.py
```
Open your browser at:
```
http://localhost:8000
```

---

## Usage

1. Enter a **topic** (e.g. "Binary Search Trees", "Linked Lists")
2. Select **difficulty** — Easy / Medium / Hard
3. Set **question counts** — MCQ, Short Answer, Long Answer
4. Choose **question style preferences** — Algorithm tracing, Comparative analysis, etc.
5. Click **Generate Paper**
6. View the structured paper with questions, answers and marking schemes

---

## Difficulty Levels

| Level | Bloom's Target | Question Style |
|---|---|---|
| Easy | Remember, Understand | Definitions, basic recall |
| Medium | Apply, Analyse | Problem solving, comparisons |
| Hard | Evaluate, Create | Algorithm design, proofs, trade-off analysis |

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Serves the ExamForge UI |
| `/generate` | POST | Generates a question paper |
| `/health` | GET | Health check |

### `/generate` request body
```json
{
  "topic": "Binary Search Trees",
  "difficulty": "hard",
  "num_mcq": 5,
  "num_short": 3,
  "num_long": 2,
  "rubric": ["Conceptual clarity", "Algorithm design", "Time/space complexity"]
}
```

---

## Notes

- `data/` and `faiss_index/` are not pushed to git — you need to add your own notes and rebuild the index after cloning
- `.env` is not pushed — you need to add your own Groq API key
- Re-run `python vector_store.py` every time you add new files to `data/`

---

## Built With

- [LangChain](https://langchain.com)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Groq](https://console.groq.com)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [Flask](https://flask.palletsprojects.com)