from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INDEX_PATH = DATA_DIR / "faiss.index"
MODEL_NAME = "all-MiniLM-L6-v2"

DATA_DIR.mkdir(exist_ok=True)


class VectorStore:


    def __init__(self) -> None:
        
        self.model = SentenceTransformer(MODEL_NAME)
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = self._load_or_create_index()

    def _load_or_create_index(self) -> faiss.IndexIDMap:

        if INDEX_PATH.exists():
            return faiss.read_index(str(INDEX_PATH))

        
        base_index = faiss.IndexFlatIP(self.dimension)
        return faiss.IndexIDMap(base_index)

    def save_index(self) -> None:

        faiss.write_index(self.index, str(INDEX_PATH))

    def embed_texts(self, texts: list[str]) -> np.ndarray:

        embeddings = self.model.encode(texts, convert_to_numpy=True)
        embeddings = embeddings.astype("float32")
        faiss.normalize_L2(embeddings)
        return embeddings

    def add_texts(self, texts: list[str], ids: list[int]) -> None:

        if not texts:
            return

        embeddings = self.embed_texts(texts)
        faiss_ids = np.array(ids, dtype="int64")
        self.index.add_with_ids(embeddings, faiss_ids)
        self.save_index()

    def search(self, query: str, k: int = 5) -> list[dict[str, float | int]]:

        if self.index.ntotal == 0:
            return []

        query_embedding = self.embed_texts([query])
        scores, ids = self.index.search(query_embedding, k)

        results: list[dict[str, float | int]] = []
        for score, chunk_id in zip(scores[0], ids[0]):
            if chunk_id == -1:
                continue
            results.append({"chunk_id": int(chunk_id), "score": float(score)})

        return results
