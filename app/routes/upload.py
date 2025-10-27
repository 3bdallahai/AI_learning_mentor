import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.utils.aws_s3 import upload_to_s3
from app.rag.text_extraction import extrcat_text_from_pdf,extract_text_from_txt
from app.rag.embedder import create_embedding, chunk_text
from app.rag.vector_store import  save_vectors
from app.db.database import get_db
from app.db import models
from sqlalchemy.orm import session

router = APIRouter(prefix="/documents", tags=["Documents"])


UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), db: session = Depends(get_db)):
    filename = file.filename
    local_path = os.path.join(UPLOAD_DIR,filename)
    
    content =await file.read()  
    #save locally
    with open(local_path,"wb") as f:   
        f.write(content)

    #upload to s3
    try:
        s3_url = upload_to_s3(local_path, filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"aws file upload failed: {str(e)}")
    

    if filename.lower().endswith(".pdf"):
        text = extrcat_text_from_pdf(local_path)
    elif filename.lower().endswith(".txt"):
        text= extract_text_from_txt(local_path)
    else:
        raise HTTPException(status_code=400, detail="ONLY pdf and txt files supported")
    
    #generate embeddings
    chunks = chunk_text(text)
    embeddings =create_embedding(chunks)
    save_vectors(embeddings, chunks, filename)

    #save metadata to db
    doc = models.Document(filename= filename, s3_url = s3_url, local_path= local_path)
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {"message": f"{filename} uploaded successfully!" , "s3_url":s3_url}


