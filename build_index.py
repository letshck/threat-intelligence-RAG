import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json

model = SentenceTransformer("all-MiniLM-L6-v2")

# Your CVE records (later this will be 10,000+ from NVD)
documents = [
    {"id": "CVE-2021-44228", "text": "Remote code execution in Apache Log4j via JNDI injection"},
    {"id": "CVE-2022-0847",  "text": "Linux kernel privilege escalation via Dirty Pipe"},
    {"id": "CVE-2021-34527", "text": "Windows Print Spooler remote code execution PrintNightmare"},
    {"id": "CVE-2021-26855", "text": "Microsoft Exchange authentication bypass and SSRF ProxyLogon"},
    {"id": "CVE-2023-23397", "text": "Outlook phishing triggers NTLM credential theft via email"},
]

# Embed all documents
texts = [d["text"] for d in documents]
embeddings = model.encode(texts)
embeddings = np.array(embeddings).astype("float32")

# Build FAISS index
dimension = embeddings.shape[1]          # 384 for MiniLM
index = faiss.IndexFlatL2(dimension)     # L2 = Euclidean distance
index.add(embeddings)                    # Add all vectors

# Save index + metadata to disk
faiss.write_index(index, "threat_index.faiss")
with open("threat_metadata.json", "w") as f:
    json.dump(documents, f)

print(f"Index built: {index.ntotal} vectors stored")