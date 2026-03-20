import chromadb
from sentence_transformers import SentenceTransformer
from app.models.schemas import ParsedSheet

model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.Client()

sessions = {}

def build_knowledge_base(parsed_sheet: ParsedSheet):
    session_id = parsed_sheet.session_id
    
    collection = chroma_client.create_collection(name=session_id)
    
    for chunk in parsed_sheet.chunks:
        embedding = model.encode(chunk.answer_text).tolist()
        collection.add(
            ids=[chunk.question_number],
            embeddings=[embedding],
            documents=[chunk.answer_text],
            metadatas=[{"question_number": chunk.question_number}]
        )
    
    sessions[session_id] = collection
    return session_id

def retrieve_relevant_chunks(session_id: str, query: str, top_k: int = 2) -> list[str]:
    if session_id not in sessions:
        raise ValueError(f"Session {session_id} not found")
    
    collection = sessions[session_id]
    query_embedding = model.encode(query).tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    return results["documents"][0]