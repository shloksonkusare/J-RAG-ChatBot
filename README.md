# J-RAG-ChatBot — Japanese Learning RAG System

A production-grade **Retrieval-Augmented Generation (RAG)** chatbot for learning Japanese, built with clean data pipelines, embeddings, and a persistent vector database, designed from day one for scalability, CI/CD, and future UI/backend integration.

---

## 📌 Project Goal

The goal of this project is to build a metadata-aware Japanese learning assistant that can:
- Explain Japanese grammar concepts
- Teach JLPT vocabulary
- Perform semantic (meaning-based) retrieval
- Serve as a strong foundation for a future LLM-powered chatbot

This project focuses on engineering correctness first:
- clean ingestion
- structured normalization
- reliable embeddings
- persistent vector storage
- strong logging and error handling

---
# ✅ Current Capabilities (Implemented)
### ✔ Data Ingestion & Normalization

- Grammar extracted from Tae Kim’s Grammar Guide (PDF)

- Vocabulary ingested from JLPT Kaggle dataset (CSV)

- Converted into a strict JSONL schema with metadata

### ✔ Metadata-Rich Schema

Each knowledge unit follows:
```
{
  "text": "...",
  "type": "grammar | vocab",
  "jlpt_level": "N1 | N2 | N3 | N4 | N5 | UNKNOWN",
  "topic": "hierarchical/topic/path",
  "source": "dataset or book name"
}
```

This enables precise retrieval, filtering, and future ranking.

### ✔ Production-Grade Engineering

- Centralized logging (logging.py)

- Custom exception handling (exception.py)

- CI/CD-friendly pipeline entry points

- Modular, testable architecture

--- 

## Final Directory Architecture (Locked)

```
J-RAG-ChatBot/
├── data/
│   ├── grammar/
│   │   ├── grammar_guide.pdf
│   │   └── grammar.jsonl
│   ├── vocab/
│   │   ├── jlpt_vocab.csv
│   │   └── vocab.jsonl
│
├── vector_store/
│   └── chroma/
│       └── (persistent vector DB files)
│
├── logs/
│   └── *.log
│
├── src/
│   ├── ingestion/
│   │   ├── pdf_loader.py
│   │   ├── csv_loader.py
│   │   └── corpus_loader.py
│   │
│   ├── processing/
│   │   ├── cleaner.py
│   │   ├── chunker.py
│   │   └── topic_extractor.py
│   │
│   ├── exporters/
│   │   └── jsonl_writer.py
│   │
│   ├── embeddings/
│   │   └── embedder.py
│   │
│   ├── vector_db/
│   │   └── chroma_client.py
│   │
│   ├── pipelines/
│   │   ├── build_dataset.py
│   │   └── build_embeddings.py
│   │
│   ├── tests/
│   │   └── manual_similarity_test.py
│   │
│   ├── exception.py
│   └── logging.py
│
├── requirements.txt
├── README.md
└── setup.py
```

# ▶️ How to Run Pipelines

#### Build Dataset (Grammar + Vocab)
```python -m src.pipelines.build_dataset```

#### Build Embeddings & Vector Store
```python -m src.pipelines.build_embeddings```

#### Manual Similarity Search Test
```python -m src.tests.manual_similarity_test```

---

## Data Sources:
1. Japanese-English Bilingual Corpus - [Kaggle](https://www.kaggle.com/datasets/team-ai/japaneseenglish-bilingual-corpus).
2. JLPT Vocabulary by Level - [Kaggle](https://www.kaggle.com/datasets/robinpourtaud/jlpt-words-by-level).
3. A Guide to Japanese Grammar by Tae Kim - [Link](https://www.amazon.com/Guide-Japanese-Grammar-approach-learning/dp/1495238962).

---

### 🚀 What’s Next (Planned)

- LLM-powered answer generation (full RAG loop)

- Metadata filtering (JLPT level, grammar-only queries)

- FastAPI backend

- UI for learners

- CI/CD automation (GitHub Actions)

### 🏁 Current Status
- Retrieval layer complete
- Embeddings complete
- Vector DB persistent
- Ready for LLM integration

This project now has a solid, real-world RAG foundation, not a demo or notebook experiment.