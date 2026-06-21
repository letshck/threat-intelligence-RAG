
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")

# Try it on some fake CVE descriptions
texts = [
    "CVE-2021-44228: Remote code execution in Apache Log4j via JNDI injection",
    "CVE-2022-0847: Linux kernel privilege escalation via Dirty Pipe vulnerability",
    "CVE-2021-34527: Windows Print Spooler remote code execution (PrintNightmare)",
]

embeddings = model.encode(texts)

print(f"Shape: {embeddings.shape}")  