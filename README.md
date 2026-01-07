# J-RAG-ChatBot — Project Progress Documentation

This document summarizes **everything completed so far** for the **Japanese RAG Chatbot**, written entirely in **Markdown**, covering architecture, pipelines, debugging, and design decisions.

---

## 📌 Project Goal

Build a **production-grade RAG (Retrieval-Augmented Generation) chatbot** for learning Japanese, with:

- Grammar explanations
- Vocabulary learning
- (Optional) Example sentences
- Metadata-aware semantic search
- CI/CD-friendly data pipelines
- Clean logging and exception handling

---

## Final Directory Architecture (Locked)

```
J-RAG-ChatBot/
├── data/
│   ├── grammar/
│   │   ├── grammar_guide.pdf
│   │   └── grammar.jsonl
│   ├── vocabulary/
|   |   └── jlpt_vocab.csv
│   │   └── jlpt_vocab.jsonl
|
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
│   ├── pipelines/
│   │   └── build_dataset.py
│   │
│   ├── tests/
│   │   └── test_schema.py
│   │
|   ├── __init__.py
│   ├── exception.py
│   └── logging.py
│
├── requirements.txt
├── README.md
└── setup.py
```

### Data Sources:
1. Japanese-English Bilingual Corpus - [Kaggle](https://www.kaggle.com/datasets/team-ai/japaneseenglish-bilingual-corpus).
2. JLPT Vocabulary by Level - [Kaggle](https://www.kaggle.com/datasets/robinpourtaud/jlpt-words-by-level).
3. A Guide to Japanese Grammar by Tae Kim - [Link](https://www.amazon.com/Guide-Japanese-Grammar-approach-learning/dp/1495238962).