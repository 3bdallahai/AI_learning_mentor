import faiss
import numpy as np
import os
import pickle

VECTORS_DIR = "app/rag/vectors"
os.makedirs(VECTORS_DIR,exist_ok=True)

def save_vectors(embeddings, chunks, doc_name):
    embeddings =np.array(embeddings).astype("float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index,f"{VECTORS_DIR}/{doc_name}.index")

    with open (f"{VECTORS_DIR}/{doc_name}_chunks.pkl","wb") as f:
        pickle.dump(chunks,f)


def load_vector(doc_name):
    index = faiss.read_index(f"{VECTORS_DIR}/{doc_name}.index")
    
    with open (f"{VECTORS_DIR}/{doc_name}_chunks.pkl","rb") as f:
        chunks = pickle.load(f)
    
    return index, chunks
