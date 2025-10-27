from transformers import AutoModelForCausalLM, AutoTokenizer
import os
import torch
from app.rag.retriever import retrieve_relevant_chunks



class Qwen_model():
    def __init__(self): 
        # Set Hugging Face cache directory
        os.environ["HF_HOME"] = "D:/HuggingFace"

        # Define cache directory
        model_name="Qwen/Qwen2.5-0.5B-Instruct"
        cache_dir = "D:/HuggingFace/hub"

        self.model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=cache_dir,low_cpu_mem_usage=True)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir, torch_dtype=torch.float16,)

        self.prompt =[]

        self.system_role = {"role": "system", "content": "You are a helpful assistant."}
        self.prompt.append(self.system_role)




    def generate_response(self,doc_name,question):
        context = retrieve_relevant_chunks(doc_name, question)
        context_str = "\n\n".join(context)
        
        user_role ={"role":"user","content": f"""
                Use *only* the information from the CONTEXT below to answer the QUESTION.

                If the answer is not present in the context, say: "I don’t have enough information to answer."

                CONTEXT:
                {context_str}

                QUESTION:
                {question}

                Please provide a concise, factual answer:
                """}
        self.prompt.append(user_role)

        text = self.tokenizer.apply_chat_template(self.prompt,tokenize=False,add_generation_prompt=True)

        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(    
            **model_inputs,
            max_new_tokens=512,
            temperature=0.01,
            top_p=0.9,
            do_sample=True)

        generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        response = response.strip().split("ASSISTANT:")[-1].strip()

        return response, context