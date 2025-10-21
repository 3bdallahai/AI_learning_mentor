from fastapi import APIRouter

router= APIRouter()

@router.get("/health")
def health_check():
    return{"status":"ok", "message":"AI Learning mentor API Running"}