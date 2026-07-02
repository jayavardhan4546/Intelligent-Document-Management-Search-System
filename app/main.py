import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.chunking import chunk_text
from app.database import (
    get_chunk_with_document,
    init_db,
    insert_chunk,
    insert_document,
    list_documents,
)
from app.text_extractor import SUPPORTED_EXTENSIONS, extract_text
from app.vector_store import VectorStore

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
STATIC_DIR = BASE_DIR / "app" / "static"
TEMPLATE_DIR = BASE_DIR / "app" / "templates"

UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="Intelligent Document Management & Search System",
    description="Semantic document search using FastAPI, Sentence Transformers, FAISS, and SQLite",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATE_DIR)


init_db()
vector_store = VectorStore()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health_check():

    return {"status": "running"}


@app.post("/upload")
def upload_document(file: UploadFile = File(...)):


    original_filename = file.filename or "uploaded_file"
    extension = Path(original_filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Supported types: {', '.join(SUPPORTED_EXTENSIONS)}",
        )

    safe_filename = f"{uuid.uuid4().hex}_{original_filename}"
    file_path = UPLOAD_DIR / safe_filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_text(file_path)
        chunks = chunk_text(text)

        if not chunks:
            raise HTTPException(status_code=400, detail="No readable text found in this file")

        document_id = insert_document(original_filename, str(file_path))

        chunk_ids: list[int] = []
        for index, chunk in enumerate(chunks):
            chunk_id = insert_chunk(document_id, index, chunk)
            chunk_ids.append(chunk_id)

        vector_store.add_texts(chunks, chunk_ids)

        return {
            "message": "Document uploaded and indexed successfully",
            "filename": original_filename,
            "document_id": document_id,
            "chunks_created": len(chunks),
        }

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@app.get("/search")
def search_documents(query: str, k: int = 5):


    if not query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty")

    matches = vector_store.search(query, k)

    results = []
    for match in matches:
        chunk_data = get_chunk_with_document(int(match["chunk_id"]))
        if chunk_data is None:
            continue

        results.append(
            {
                "score": round(float(match["score"]), 4),
                "filename": chunk_data["filename"],
                "document_id": chunk_data["document_id"],
                "chunk_id": chunk_data["chunk_id"],
                "chunk_index": chunk_data["chunk_index"],
                "content": chunk_data["content"],
                "uploaded_at": chunk_data["created_at"],
            }
        )

    return {"query": query, "results_count": len(results), "results": results}


@app.get("/documents")
def get_documents():

    return {"documents": list_documents()}
