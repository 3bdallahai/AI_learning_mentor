import os
from fastapi import APIRouter , HTTPException
from app.rag.vector_store import VECTORS_DIR

router = APIRouter(prefix="/api/documents", tags=["Documents"])

@router.get("/")
def list_doc():
    files = [f.replace(".index","") for f in os.listdir(VECTORS_DIR) if f.endswith(".index") ]
    return {"document": files}

@router.delete("/{doc_name}")
def delete_document(doc_name:str):
    index_path = os.path.join(VECTORS_DIR,f"{doc_name}.index")
    chunks_path = os.path.join(VECTORS_DIR,f"{doc_name}_chunks.pkl")

    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Document not found")
    
    os.remove(index_path)

    if os.path.exists(chunks_path):
        os.remove(chunks_path)

    return {"message": f"'{doc_name}' deleted successfully"}


