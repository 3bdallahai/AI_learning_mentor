import faiss
import numpy as np
import os
import io
import pickle
from app.utils.aws_s3 import get_s3_client,settings

VECTORS_DIR = "app/rag/vectors"
os.makedirs(VECTORS_DIR,exist_ok=True)

s3 = get_s3_client()
bucket_name = settings.AWS_BUCKET_NAME

def save_vectors(embeddings, chunks, doc_name):
    embeddings =np.array(embeddings).astype("float32")
    norm = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings =embeddings/norm
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    index_buffer = faiss.serialize_index(index)
    s3.upload_fileobj(io.BytesIO(index_buffer),bucket_name,f"vectors/{doc_name}.index")

    chunks_buffer = io.BytesIO()
    pickle.dump(chunks, chunks_buffer)
    chunks_buffer.seek(0)
    s3.upload_fileobj(chunks_buffer, bucket_name, f"vectors/{doc_name}_chunks.pkl")

    print(f"successfully uploaded {doc_name} vector to s3")


def load_vector(doc_name):
    index_stream = io.BytesIO()
    s3.download_fileobj(bucket_name, f"vectors/{doc_name}.index", index_stream)
    index_stream.seek(0)
    index_bytes = index_stream.read()
    index = faiss.deserialize_index(np.frombuffer(index_bytes, dtype=np.uint8))

    # Download chunks into memory
    chunks_stream = io.BytesIO()
    s3.download_fileobj(bucket_name, f"vectors/{doc_name}_chunks.pkl", chunks_stream)
    chunks_stream.seek(0)
    chunks = pickle.load(chunks_stream)

    return index, chunks
