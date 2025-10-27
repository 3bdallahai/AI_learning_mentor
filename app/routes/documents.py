import os
from fastapi import APIRouter , HTTPException, Depends
from app.rag.vector_store import VECTORS_DIR
from sqlalchemy.orm import session
from app.db.database import get_db
from app.db import models
from app.utils.aws_s3 import delete_from_s3

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.get("/")
def list_doc(db: session= Depends(get_db)):
    docs = db.query(models.Document).all()
    
    return [{"id":d.id, "filename": d.filename, "s3_url":d.s3_url} for d in docs ]

@router.delete("/{doc_name}")
def delete_document(doc_name:str, db:session=Depends(get_db)):

    index_path = os.path.join(VECTORS_DIR, f"{doc_name}.index")
    chunks_path = os.path.join(VECTORS_DIR, f"{doc_name}_chunks.pkl")


    doc = db.query(models.Document).filter(models.Document.filename == doc_name).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        delete_from_s3(doc.s3_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed to delete from s3:{str(e)} ")
    
    os.remove(index_path)

    if os.path.exists(chunks_path):
        os.remove(chunks_path)

    deleted_rows = db.query(models.Document).filter(models.Document.filename == doc_name).delete()
    db.commit()

    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="Document not found in database")


    return {"message": f"'{doc_name}' deleted successfully"}


