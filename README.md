# J-RAG-ChatBot — Japanese Learning RAG System

A production-grade **Retrieval-Augmented Generation (RAG)** system for learning Japanese, built with clean data pipelines, metadata-aware retrieval, embeddings, translation support, and LLM-based answer generation.

This project is designed from day one for:

- scalability

- CI/CD

- backend & UI integration

- real-world RAG correctness (not a demo)

## 📌 Project Goal

The goal of this project is to build a metadata-aware Japanese learning assistant that can:

- Explain Japanese grammar concepts (e.g. は vs が)

- Teach JLPT vocabulary

- Perform semantic (meaning-based) retrieval

- Support multilingual input (Japanese / English)

- Generate grounded answers using an LLM

This project focuses on engineering correctness first:

- clean ingestion

- structured normalization

- reliable embeddings

- persistent vector storage

- strong logging & exception handling

- modular, extensible architecture

## Current Capabilities (Implemented)
- Data Ingestion & Normalization

  - Grammar extracted from Tae Kim’s Grammar Guide (PDF)

  - Vocabulary ingested from JLPT Kaggle dataset (CSV)

  - Converted into a strict JSONL schema with metadata

  - Chunked and cleaned for semantic retrieval

##  Metadata-Rich Schema

Each knowledge unit follows a strict format:
```
{
  "text": "...",
  "type": "grammar | vocab",
  "jlpt_level": "N1 | N2 | N3 | N4 | N5 | UNKNOWN",
  "topic": "hierarchical/topic/path",
  "source": "dataset or book name"
}
```


This enables:

- grammar-only retrieval

- JLPT-aware filtering

- topic-based routing

- future ranking and re-scoring

## Embeddings & Vector Database

- Multilingual embeddings generated using Sentence Transformers

- Persistent ChromaDB vector store

- Disk-backed storage (no re-embedding required on restart)

- Batched ingestion for scalability

- Metadata-aware similarity search

## Translation Layer (Free & Offline)

- Japanese → English translation for query normalization

- Implemented using MarianMT / Fugumt models

- No API keys required

- CPU-friendly

- Cleanly isolated translation module

- Used only where appropriate (input normalization), not for reasoning.

## LLM-Powered Answer Generation (Full RAG Loop)

- Integrated Groq LLM API for fast, high-quality reasoning

- Context-grounded answer generation

- Retrieval + reasoning combined end-to-end

- .env-based secret management (no hardcoded keys)

- Prompt designed for factual, grounded explanations

## Production-Grade Engineering

- Centralized logging (login.py)

- Custom exception handling with traceability (exception.py)

- CI/CD-friendly pipeline entry points

- Layered architecture (ingestion → processing → embeddings → retrieval → LLM)

- Debugged real-world dependency & environment issues (Windows, Python, ML stack)

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
│   ├── translation/
│   │   └── translator.py
│   │
│   ├── llm/
│   │   └── answer_generator.py
│   │
│   ├── rag/
│   │   └── rag_pipeline.py
│   │
│   ├── pipelines/
│   │   ├── build_dataset.py
│   │   └── build_embeddings.py
│   │
│   ├── tests/
│   │   ├── manual_similarity_test.py
│   │   └── test_rag_pipeline.py
│   │
│   ├── exception.py
│   └── logging.py
│
├── .env
├── requirements.txt
├── README.md
└── setup.py
```

## How to Run Pipelines
- Build Dataset (Grammar + Vocabulary)
```python -m src.pipelines.build_dataset```

- Build Embeddings & Vector Store
```python -m src.pipelines.build_embeddings```

- Manual Similarity Search Test
```python -m src.tests.manual_similarity_test```

- End-to-End RAG Test (Retrieval + LLM)
```python -m src.tests.test_rag_pipeline```

🔐 Environment Variables

Create a .env file in the project root:

```GROQ_API_KEY=your_api_key_here```


.env is excluded via .gitignore

📚 Data Sources

1. Japanese-English Bilingual Corpus — Kaggle
https://www.kaggle.com/datasets/team-ai/japaneseenglish-bilingual-corpus

2. JLPT Vocabulary by Level — Kaggle
https://www.kaggle.com/datasets/robinpourtaud/jlpt-words-by-level

3. A Guide to Japanese Grammar — Tae Kim
https://www.amazon.com/dp/1495238962