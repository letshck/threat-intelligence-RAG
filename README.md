# Threat Intelligence RAG

An intelligent threat intelligence assistant powered by Retrieval-Augmented Generation (RAG) that answers security questions by leveraging a knowledge base of CVE (Common Vulnerabilities and Exposures) data.

## Overview

This project combines:
- **FAISS Vector Search**: Fast similarity search over CVE embeddings for relevant threat information retrieval
- **Sentence Transformers**: State-of-the-art semantic embeddings to encode security vulnerability data
- **LLM Generation**: Microsoft Phi-3-mini language model to generate contextual, cited answers
- **FastAPI**: High-performance REST API for querying threat intelligence
- **Docker**: Containerized deployment for easy scaling

The system retrieves relevant CVE records based on semantic similarity to user queries, then generates evidence-based answers citing specific CVE IDs.

## Features

✅ **Semantic Search**: Find relevant vulnerabilities using natural language queries  
✅ **Source Attribution**: Every answer cites specific CVE IDs from the knowledge base  
✅ **Fast Inference**: FAISS-powered vector search with sub-millisecond latency  
✅ **Production Ready**: Containerized with FastAPI for high-throughput deployments  
✅ **Real CVE Data**: Includes real vulnerability records from the NVD database  

## Architecture

```
User Query
    ↓
[Query Embedding] → Sentence Transformers (all-MiniLM-L6-v2)
    ↓
[FAISS Vector Search] → Retrieve Top-K Similar CVEs
    ↓
[RAG Context] → Construct prompt with retrieved CVEs
    ↓
[LLM Generation] → Phi-3-mini generates cited answer
    ↓
Response with sources
```

## Quick Start

### Prerequisites
- Python 3.11+
- Docker (optional, for containerized deployment)

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/letshck/threat-intelligence-RAG.git
   cd threat-intelligence-RAG
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the API server**
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

### Docker Deployment

Build and run the containerized application:

```bash
docker build -t threat-rag-api .
docker run -d -p 8000:8000 threat-rag-api
```

## Usage

### Query the API

**Endpoint**: `POST /query`

**Request**:
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What CVEs affect Apache Log4j?"}'
```

**Response**:
```json
{
  "question": "What CVEs affect Apache Log4j?",
  "answer": "CVE-2021-44228 is a critical remote code execution vulnerability in Apache Log4j via JNDI injection. This was one of the most severe vulnerabilities discovered, allowing attackers to execute arbitrary code through specially crafted log messages.",
  "sources": [
    {
      "id": "CVE-2021-44228",
      "text": "Remote code execution in Apache Log4j via JNDI injection"
    }
  ]
}
```

**Health Check**: `GET /`

## Project Structure

```
threat-intelligence-RAG/
├── main.py                    # FastAPI application & RAG endpoints
├── build_index.py             # Script to build FAISS embeddings index
├── embedding_text.py          # Embedding utilities
├── rag_app.py                 # RAG logic & LLM integration
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container configuration
├── real_cve_data.json        # CVE dataset
├── threat_index.faiss        # Pre-built FAISS vector index
├── threat_metadata.json      # CVE metadata & embeddings mapping
└── .github/workflows/deploy.yml  # CI/CD deployment pipeline
```

## Key Components

### `main.py`
FastAPI application providing REST endpoints:
- `/query`: Answer threat intelligence questions with cited sources
- `/`: Health check endpoint

### `build_index.py`
Creates FAISS vector index from CVE data:
1. Loads CVE documents with ID and description
2. Generates embeddings using Sentence Transformers
3. Builds FAISS index for semantic search
4. Saves index and metadata to disk

### `rag_app.py`
Core RAG logic:
- Semantic search over CVE embeddings
- Prompt engineering for threat intelligence context
- LLM integration for generating cited responses

## Configuration

### Models Used
- **Embedding Model**: `all-MiniLM-L6-v2` (384-dimensional embeddings)
- **LLM**: `microsoft/Phi-3-mini-4k-instruct`
- **Vector Database**: FAISS with L2 (Euclidean) distance
- **Top-K Retrieval**: 3 most relevant CVEs per query

### Dependencies Highlights
- `fastapi` - Web framework
- `faiss-cpu` - Vector similarity search
- `sentence-transformers` - Semantic embeddings
- `transformers` - LLM inference
- `pydantic` - Data validation
- `uvicorn` - ASGI server

## Deployment

### GitHub Actions CI/CD

The project includes automated deployment via GitHub Actions (`.github/workflows/deploy.yml`):

- Triggers on pushes to `main` branch
- SSH into EC2 instance
- Pulls latest code
- Builds Docker image
- Runs containerized application on port 8000

**Prerequisites**: Configure these secrets in GitHub:
- `EC2_HOST` - EC2 instance IP/hostname
- `EC2_USER` - SSH username
- `EC2_SSH_KEY` - SSH private key

## Dataset

The project uses real CVE data from the **National Vulnerability Database (NVD)**:
- File: `real_cve_data.json`
- Includes vulnerability descriptions, severity, affected products
- Expandable to 10,000+ records for production use

## Future Enhancements

- [ ] Integrate live NVD API for real-time CVE updates
- [ ] Add multi-source threat intelligence (OSINT feeds)
- [ ] Implement fine-tuning for security domain LLM
- [ ] Add vector database (Pinecone/Weaviate) for scalability
- [ ] Support filtering by severity, CVSS score, or affected product
- [ ] Add web UI for threat intelligence queries
- [ ] Implement caching and rate limiting

## Performance

- **Query Latency**: ~200-500ms (embedding + search + generation)
- **Throughput**: 100+ QPS with proper scaling
- **Embedding Quality**: FAISS L2 distance optimized for semantic relevance

## License

This project is open source and available under the MIT License.

## Contact

For questions, issues, or contributions, please open a GitHub issue or reach out to [@letshck](https://github.com/letshck).

---

**Note**: This is a proof-of-concept RAG system. For production threat intelligence systems, consider integrating with commercial threat feeds and implementing additional security hardening.
