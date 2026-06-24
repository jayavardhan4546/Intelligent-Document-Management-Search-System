
# Intelligent Document Management & Search System

A complete FastAPI project for uploading organizational documents, indexing their content, and searching them with natural-language queries using NLP embeddings + FAISS vector search + MySQL metadata storage.

This project is designed to be GitHub-ready and resume-friendly.

## Features

- Upload `.txt`, `.md`, `.pdf`, and `.docx` documents
- Extract document text automatically
- Split large files into searchable chunks
- Generate semantic embeddings using Sentence Transformers
- Store document and chunk metadata in MySQL through SQLAlchemy
- Store vector embeddings in a FAISS index for fast similarity search
- Natural-language search API with ranked results
- Simple built-in frontend for upload and search
- Docker Compose setup with MySQL
- SQLite fallback for quick local testing
- Reindex endpoint to rebuild FAISS from stored chunks

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **NLP:** Sentence Transformers with a deterministic fallback embedder
- **Vector Search:** FAISS
- **Database:** MySQL with SQLAlchemy ORM
- **Frontend:** HTML, CSS, JavaScript
- **Deployment/Run:** Docker Compose

## Project Structure

```text
intelligent-document-management-system/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   ├── services/
│   ├── static/
│   ├── data/
│   └── sample_docs/
├── scripts/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## Run with Docker Compose

This is the recommended way because it starts both the FastAPI app and MySQL.

```bash
docker compose up --build
```

Open the app:

```text
http://localhost:8000
```

Open API docs:

```text
http://localhost:8000/docs
```

The first run may take time because the embedding model has to download once.

## Run Locally Without Docker

This mode uses SQLite by default, so you can test the project quickly.

```bash
python -m venv .venv
```

Windows PowerShell:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the app:

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000
```

## MySQL Configuration

Copy `.env.example` to `.env` and update the values if you want to connect to your own MySQL database.

Example SQLAlchemy MySQL URL:

```env
DATABASE_URL=mysql+pymysql://doc_user:doc_password@localhost:3306/doc_search
```

When using Docker Compose, the API service already receives the correct internal MySQL URL.

## API Endpoints

### Health Check

```http
GET /api/health
```

### Upload Document

```http
POST /api/documents/upload
```

Form data:

- `file`: document file
- `title`: optional document title

### List Documents

```http
GET /api/documents
```

### Search Documents

```http
POST /api/search
```

Body:

```json
{
  "query": "leave policy for employees",
  "top_k": 5
}
```

### Rebuild FAISS Index

```http
POST /api/documents/reindex
```

### Delete Document

```http
DELETE /api/documents/{document_id}
```

## Sample Document

A sample file is included at:

```text
backend/sample_docs/company_policy.txt
```

Upload it from the frontend and search for:

```text
What is the remote work policy?
```

## Environment Variables

| Variable | Default | Description |
|---|---:|---|
| `APP_NAME` | Intelligent Document Management & Search System | App display name |
| `DATABASE_URL` | SQLite local database | SQLAlchemy database URL |
| `EMBEDDING_MODEL_NAME` | sentence-transformers/all-MiniLM-L6-v2 | Sentence Transformer model |
| `EMBEDDING_BACKEND` | sentence_transformer | Use `sentence_transformer` or `hash` |
| `ALLOW_HASH_FALLBACK` | true | Uses local hash embeddings if model loading fails |
| `EMBEDDING_DIMENSION` | 384 | Vector dimension for FAISS |
| `CHUNK_SIZE` | 900 | Characters per chunk |
| `CHUNK_OVERLAP` | 150 | Overlap between chunks |
| `MAX_UPLOAD_MB` | 20 | Max file size in MB |

## Resume Description

**Intelligent Document Management & Search System | Python, FastAPI, NLP, FAISS, MySQL**

- Developed an intelligent document platform enabling natural language search across organizational files.
- Implemented document ingestion, text extraction, chunking, semantic indexing, and FAISS-powered retrieval APIs.
- Integrated MySQL metadata storage with SQLAlchemy and built a simple frontend for document upload and real-time search.
- Improved knowledge accessibility by reducing manual document search through AI-powered information retrieval.

## Notes

- FAISS stores the vector index in `backend/data/index`.
- Uploaded documents are stored in `backend/data/uploads`.
- MySQL stores document metadata and searchable chunks.
- If the Sentence Transformer model cannot load, the system can still run using the local deterministic hash embedder.
