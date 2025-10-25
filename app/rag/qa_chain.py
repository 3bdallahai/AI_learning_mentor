from transformers import pipeline
from app.rag.retriever import retrieve_relevant_chunks
import os

# Set Hugging Face cache directory
os.environ["HF_HOME"] = "D:/HuggingFace"

# Define cache directory
model_name="Qwen/Qwen2.5-0.5B-Instruct"
cache_dir = "D:/HuggingFace/hub"

qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

def generate_answer(doc_name,question):
    context_chunks = retrieve_relevant_chunks(doc_name, question)
    answers = []
    
    for chunk in context_chunks:
        result = qa_pipeline(question,chunk)
        answers.append(
            {
                "answer": result["answer"],
                "score": result["score"],
                "context": chunk
            }
        ) 

        best = max(answers, key=lambda x:x["score"] )

        return  {
        "final_answer": best["answer"],
        "context_used": [a["context"] for a in answers]
    }