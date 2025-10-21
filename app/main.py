from fastapi import FastAPI
from app.db import models
from app.db.database import engine
from app.routes import health
from app.utils import aws_s3
#create tables in MySQL 
models.base.metadata.create_all(bind= engine)

app = FastAPI(title= "AI Learning mentor API")

#Include routes
app.include_router(health.router, prefix="/api")



@app.get("/")
def root():
    return {"message":"Welcome to AI Engineering Mentor API"}

