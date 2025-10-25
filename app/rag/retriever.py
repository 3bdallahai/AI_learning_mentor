import numpy as np
from app.rag.vector_store import load_vector
from app.rag.embedder import create_embedding

def retrieve_relevant_chunks(doc_name,query,top_k=3):
    index, chunks = load_vector(doc_name)

    query_vector = np.array(create_embedding([query])).astype("float32")

    _,indices = index.search(query_vector,top_k)

    retrieved_chunks = [chunks[i] for i in indices[0]]

    return retrieved_chunks
