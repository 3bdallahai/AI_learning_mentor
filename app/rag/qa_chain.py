from app.Qwen_model.model import Qwen_model

model = Qwen_model()

def generate_answer(doc_name,question):

    result,context = model.generate_response(doc_name,question)

    return  {
    "final_answer": result,
    "context_used": context
}