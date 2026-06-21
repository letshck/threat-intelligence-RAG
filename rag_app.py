import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json
from transformers import pipeline

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load saved index + metadata
index = faiss.read_index("threat_index.faiss")
with open("threat_metadata.json") as f:
    documents = json.load(f)

generator = pipeline("text-generation", model="microsoft/Phi-3-mini-4k-instruct", device_map="auto")
generator.model.generation_config.max_length = None

def search(query, top_k=3):
    query_vec = embed_model.encode([query]).astype("float32")
    distances, indices = index.search(query_vec, top_k)
    results = [documents[idx] for idx in indices[0]]
    return results

def ask(query):
    results = search(query)
    print("DEBUG - search results:", results)

    context = "\n".join([f"- [{r['id']}] {r['text']}" for r in results])
    prompt = f"""You are a threat intelligence assistant. Answer the question using ONLY the CVE data below. Cite the CVE ID for every claim.
CVE Data:
{context}

Question: {query}
Answer:"""
    print("DEBUG - prompt built, length:", len(prompt))

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
    print("DEBUG - full_text:", repr(full_text))

    generated_only = full_text[len(prompt):]
    answer_part = generated_only.split("Question:")[0]

    return answer_part.strip()

if __name__ == "__main__":
    answer = ask("what vulnerabilities allow remote code execution?")
    print("\nFINAL ANSWER:")
    print(answer)