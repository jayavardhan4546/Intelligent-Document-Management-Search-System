# Intelligent Document Management & Search System

I built this project as a backend-focused intelligent document search system. The application allows users to upload documents and search their content using semantic meaning instead of only keyword matching.

## Overview

The system works in two phases:

1. Document ingestion: uploaded files are saved, text is extracted, text is split into chunks, embeddings are generated, vectors are stored in FAISS, and metadata is stored in SQLite.
2. Semantic search: the user query is converted into an embedding, FAISS finds the closest document chunks, and SQLite returns the actual document text and file details.

## Tech Stack

- Python
- FastAPI
- Sentence Transformers
- FAISS
- SQLite
- HTML
- CSS
- JavaScript

## Features

- Upload TXT, PDF, and DOCX files
- Extract readable text from documents
- Split large documents into smaller chunks
- Generate semantic embeddings using Sentence Transformers
- Store and search vectors using FAISS
- Store document metadata and text chunks in SQLite
- Search documents using natural language queries
- View uploaded documents and matching chunks from the browser

## Project Structure

```text
intelligent_doc_search_system/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── text_extractor.py
│   ├── chunking.py
│   ├── vector_store.py
│   ├── static/
│   │   ├── script.js
│   │   └── style.css
│   └── templates/
│       └── index.html
├── data/
├── uploads/
├── sample_documents/
├── requirements.txt
└── README.md
```

## How It Works

### Upload Flow

```text
User uploads file
→ FastAPI receives file
→ File is saved locally
→ Text is extracted
→ Text is split into chunks
→ Chunks are stored in SQLite
→ Chunks are converted into embeddings
→ Embeddings are stored in FAISS
```

### Search Flow

```text
User enters query
→ Query is converted into embedding
→ FAISS searches similar vectors
→ Matching chunk IDs are returned
→ SQLite fetches actual text and metadata
→ Results are returned to the browser
```

## Supported File Types

- `.txt`
- `.pdf`
- `.docx`

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```bash
.venv\Scripts\activate
```

Activate the virtual environment on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn app.main:app --reload
```

Open the browser:

```text
http://127.0.0.1:8000
```

FastAPI API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Opens the browser interface |
| GET | `/health` | Checks backend status |
| POST | `/upload` | Uploads and indexes a document |
| GET | `/search` | Searches indexed documents |
| GET | `/documents` | Lists uploaded documents |

## Notes

The embedding model is loaded using Sentence Transformers. On the first run, the model may be downloaded automatically and cached locally by the library. FAISS index files and SQLite database files are generated inside the `data` folder during runtime.
