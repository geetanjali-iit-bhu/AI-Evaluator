"""
vector_store.py
Builds the FAISS vector store from ingested documents and saves it to disk.
Run this once (or whenever the professor uploads new material).
"""

import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from ingestion import load_documents

INDEX_DIR = "faiss_index"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)


def build_vector_store(source_dir: str = "data") -> FAISS:
    """Load docs → embed → build FAISS index → save to disk."""
    print("Loading documents …")
    docs = load_documents(source_dir)

    if not docs:
        raise ValueError(
            f"No documents found in '{source_dir}'. "
            "Add PDFs, PPTX, DOCX, or TXT files there first."
        )

    print(f"\nBuilding FAISS index from {len(docs)} chunks …")
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(docs, embeddings)

    os.makedirs(INDEX_DIR, exist_ok=True)
    vector_store.save_local(INDEX_DIR)
    print(f"✓ Index saved to '{INDEX_DIR}/'")
    return vector_store


def load_vector_store() -> FAISS:
    """Load an existing FAISS index from disk."""
    if not os.path.exists(INDEX_DIR):
        raise FileNotFoundError(
            f"No index found at '{INDEX_DIR}/'. Run build_vector_store() first."
        )
    embeddings = get_embeddings()
    return FAISS.load_local(
        INDEX_DIR,
        embeddings,
        allow_dangerous_deserialization=True,
    )


def retrieve_chunks(vector_store: FAISS, query: str, k: int = 5) -> list:
    """Return the top-k most relevant chunks for a query."""
    return vector_store.similarity_search(query, k=k)


if __name__ == "__main__":
    build_vector_store("data")