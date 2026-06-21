from fastapi import FastAPI
from pydantic import BaseModel
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json
from transformers import pipeline

app = FastAPI()

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("threat_index.faiss")
with open("threat_metadata.json") as f:
    documents = json.load(f)

generator = pipeline("text-generation", model="microsoft/Phi-3-mini-4k-instruct", device_map="auto")
generator.model.generation_config.max_length = None

class QueryRequest(BaseModel):
    question: str

def search(query, top_k=3):
    query_vec = embed_model.encode([query]).astype("float32")
    distances, indices = index.search(query_vec, top_k)
    results = [documents[idx] for idx in indices[0]]
    return results

def ask(query):
    results = search(query)
    context = "\n".join([f"- [{r['id']}] {r['text']}" for r in results])
    prompt = f"""You are a threat intelligence assistant. Answer the question using ONLY the CVE data below. Cite the CVE ID for every claim.
CVE Data:
{context}

Question: {query}
Answer:"""

    response = generator(
        prompt,
        max_new_tokens=200,
        do_sample=False,
        eos_token_id=generator.tokenizer.eos_token_id,
        pad_token_id=generator.tokenizer.eos_token_id,
        truncation=True,
        clean_up_tokenization_spaces=True
    )

    full_text = response[0]["generated_text"]
    generated_only = full_text[len(prompt):]
    answer_part = generated_only.split("Question:")[0]
    return answer_part.strip(), results

@app.post("/query")
def query_endpoint(request: QueryRequest):
    answer, sources = ask(request.question)
    return {
        "question": request.question,
        "answer": answer,
        "sources": sources
    }

@app.get("/")
def health_check():
    return {"status": "RAG API is running"}