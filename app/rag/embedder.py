from sentence_transformers import SentenceTransformer
import textwrap

model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, chunk_size=500):
    return textwrap.wrap(text, chunk_size)

def create_embedding(chuncks):
    embedding = model.encode(chuncks)
    return embedding

