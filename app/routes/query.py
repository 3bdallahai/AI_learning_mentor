from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.rag.qa_chain import generate_answer



router = APIRouter()


class QueryRequest(BaseModel):
    doc_name: str
    question: str

@router.post("/query")
async def query_document(request: QueryRequest):

    try:
        response = generate_answer(request.doc_name, request.question)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"query processing failed: {str(e)}")