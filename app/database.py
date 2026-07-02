import sqlite3
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "documents.db"

DATA_DIR.mkdir(exist_ok=True)


def get_connection() -> sqlite3.Connection:

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER NOT NULL,
            chunk_index INTEGER NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (document_id) REFERENCES documents(id)
        )
        """
    )

    conn.commit()
    conn.close()


def insert_document(filename: str, file_path: str) -> int:

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO documents (filename, file_path) VALUES (?, ?)",
        (filename, file_path),
    )

    document_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return int(document_id)


def insert_chunk(document_id: int, chunk_index: int, content: str) -> int:

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chunks (document_id, chunk_index, content)
        VALUES (?, ?, ?)
        """,
        (document_id, chunk_index, content),
    )

    chunk_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return int(chunk_id)


def get_chunk_with_document(chunk_id: int) -> dict[str, Any] | None:

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            chunks.id AS chunk_id,
            chunks.chunk_index,
            chunks.content,
            documents.id AS document_id,
            documents.filename,
            documents.file_path,
            documents.created_at
        FROM chunks
        JOIN documents ON chunks.document_id = documents.id
        WHERE chunks.id = ?
        """,
        (chunk_id,),
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return dict(row)


def list_documents() -> list[dict[str, Any]]:

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            documents.id,
            documents.filename,
            documents.file_path,
            documents.created_at,
            COUNT(chunks.id) AS chunk_count
        FROM documents
        LEFT JOIN chunks ON documents.id = chunks.document_id
        GROUP BY documents.id
        ORDER BY documents.created_at DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
