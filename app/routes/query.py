from fastapi import APIRouter, HTTPException,Depends
from pydantic import BaseModel
from sentence_transformers import util
from app.rag.qa_chain import generate_answer
from app.db.models import QueryCache
from sqlalchemy.orm import session
from app.db.database import get_db
from app.rag.embedder import model
import json



router = APIRouter()


class QueryRequest(BaseModel):
    doc_name: str
    question: str

@router.post("/query")
async def query_document(request: QueryRequest, db: session = Depends(get_db)):
    question = request.question

    cached = db.query(QueryCache).all()

    question_emb =  model.encode(question, convert_to_tensor=True)
    for c in cached:
        cache_emb = model.encode(c.question, convert_to_tensor=True)
        sim = util.cos_sim(cache_emb,question_emb).item()
        if sim> 0.85:
            return {"answer": c.answer, "source": "cache", "similarity": sim }



    try:
        response = generate_answer(request.doc_name,question)

        entry = QueryCache(
            question=question,
            answer=json.dumps(response["final_answer"]),
            embedding_path=response.get("embedding_path"),

        )
        db.add(entry)
        db.commit()

        print(response)
        return {"answer":response, "source":"llm"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"query processing failed: {str(e)}")
    