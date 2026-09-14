# RAG — AI-Powered Knowledge Assistant

An AI-powered Retrieval-Augmented Generation (RAG) system designed to answer questions from a collection of internal documents using semantic search, vector embeddings, and Large Language Models.

The system combines document processing, vector search, and LLM-based response generation to provide relevant, context-aware answers grounded in the available knowledge base.

---

## Overview

Traditional LLM applications can generate answers without having access to an organization's private or domain-specific information.

This project addresses that limitation using **Retrieval-Augmented Generation (RAG)**.

Instead of relying only on the language model's pre-trained knowledge, the system:

1. Processes uploaded documents.
2. Extracts and prepares their content.
3. Generates vector embeddings.
4. Stores the embeddings in a vector database.
5. Retrieves the most relevant information for a user's question.
6. Provides the retrieved context to an LLM.
7. Generates an answer based on the retrieved information.

### Architecture

```text
                ┌─────────────────────┐
                │       User          │
                │   Ask a Question    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    FastAPI Backend   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   Query Processing   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   Vector Search      │
                │     pgvector         │
                └──────────┬──────────┘
                           │
                  Relevant Context
                           │
                           ▼
                ┌─────────────────────┐
                │        LLM          │
                │  Response Generation│
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   Grounded Answer   │
                └─────────────────────┘
```

---

## Key Features

### Document Processing

The system supports processing documents and preparing their content for semantic retrieval.

The processing pipeline includes:

* Document ingestion
* Text extraction
* Content preprocessing
* Text chunking
* Embedding generation
* Vector storage

### Semantic Search

Instead of matching questions using exact keywords, the system uses semantic similarity to retrieve information that is conceptually relevant to the user's query.

### Retrieval-Augmented Generation

Retrieved document chunks are provided to the language model as contextual information before generating the final response.

This helps the system produce answers that are more closely grounded in the available documents.

### Vector Database

Document embeddings are stored in a vector database using **PostgreSQL + pgvector**, allowing efficient similarity-based retrieval.

### LLM Provider Architecture

The project uses a provider-based architecture for language models.

This makes it possible to integrate different LLM providers without tightly coupling the application to a single provider.

### Background Processing

Long-running operations such as data processing and indexing can be handled through **Celery workers**, allowing these tasks to run independently from the API server.

### API-Based Backend

The backend is implemented using **FastAPI** and exposes endpoints for application functionality such as data processing and retrieval.

---

## Technology Stack

### Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* Alembic

### AI / NLP

* Large Language Models (LLMs)
* Retrieval-Augmented Generation (RAG)
* Text Embeddings
* Semantic Search
* Natural Language Processing

### Database

* PostgreSQL
* pgvector

### Background Processing

* Celery
* Celery Beat
* Flower

### Infrastructure

* Docker
* Docker Compose

### Development

* Git
* GitHub
* Linux / WSL
* Postman

---

## Project Structure

```text
mini-rag/
│
├── docker/
│   ├── docker-compose.yml
│   ├── minirag/
│   │   ├── Dockerfile
│   │   └── entrypoint.sh
│   └── ...
│
├── src/
│   ├── controllers/
│   ├── helpers/
│   ├── routes/
│   ├── stores/
│   │   ├── llm/
│   │   │   └── providers/
│   │   └── vectordb/
│   ├── tasks/
│   ├── main.py
│   ├── celery_app.py
│   ├── requirements.txt
│   └── ...
│
├── .github/
├── .vscode/
├── LICENSE
└── README.md
```

---

## RAG Pipeline

The core workflow of the application can be summarized as follows:

```text
Documents
    │
    ▼
Document Processing
    │
    ▼
Text Extraction
    │
    ▼
Text Chunking
    │
    ▼
Embedding Generation
    │
    ▼
Vector Database
    │
    ▼
User Query
    │
    ▼
Query Embedding
    │
    ▼
Semantic Similarity Search
    │
    ▼
Relevant Chunks
    │
    ▼
LLM Context
    │
    ▼
Generated Answer
```

---

## Environment Configuration

The application uses environment variables for configuration.

Create an environment file based on the provided example:

```bash
cp .env.example .env
```

Configure the required values in the `.env` file.

For example:

```env
OPENAI_API_KEY=your_api_key
```

Additional configuration may be required depending on the selected LLM and database providers.

> **Security:** Never commit API keys, passwords, tokens, or other sensitive credentials to GitHub.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ShahdNazzal/RAG.git
cd RAG
```

### 2. Create the Python environment

Python 3.10 is recommended.

Using Conda:

```bash
conda create -n mini-rag python=3.10
conda activate mini-rag
```

### 3. Install dependencies

```bash
pip install -r src/requirements.txt
```

### 4. Configure environment variables

Create the required `.env` files using the provided examples and configure the necessary credentials.

---

## Running with Docker

Move to the Docker directory:

```bash
cd docker
```

Start the services:

```bash
sudo docker compose up -d
```

To check the running containers:

```bash
docker ps
```

---

## Running the API

From the `src` directory:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

The API will be available at:

```text
http://localhost:5000
```

---

## Celery

### Start a Celery Worker

```bash
python -m celery -A celery_app worker \
--queues=default,file_processing,data_indexing \
--loglevel=info
```

### Start Celery Beat

```bash
python -m celery -A celery_app beat \
--loglevel=info
```

### Start Flower

```bash
python -m celery -A celery_app flower \
--conf=flowerconfig.py
```

Flower can then be accessed through:

```text
http://localhost:5555
```

---

## Available Services

When running the complete Docker environment, the main services include:

| Service    |                      Port |
| ---------- | ------------------------: |
| FastAPI    |                    `5000` |
| Flower     |                    `5555` |
| Grafana    |                    `3000` |
| Prometheus |                    `9090` |
| PostgreSQL | Configured through Docker |

---

## API Testing

The backend APIs can be tested using **Postman**.

A Postman collection can be used to test the available endpoints and the application's data-processing workflow.

---

## Engineering Concepts Demonstrated

This project was developed as a practical implementation of several modern AI engineering concepts:

* Retrieval-Augmented Generation
* LLM integration
* Embedding-based information retrieval
* Vector databases
* Semantic search
* REST API development
* FastAPI
* Database migrations
* PostgreSQL
* pgvector
* Background task processing
* Celery
* Dockerized services
* Modular provider architecture
* Environment-based configuration

---

## Learning & Development

This project was developed as part of hands-on learning in **RAG, LLM application development, backend engineering, vector databases, and AI engineering**.

The implementation was adapted and extended while studying these concepts, with additional development and experimentation performed throughout the project.

The project structure and implementation reflect practical work with the technologies listed above.

---

## Author

**Shahed Nazzal**

Artificial Intelligence & Data Science Graduate

GitHub:
https://github.com/ShahdNazzal

---

## License

This project is provided for educational and development purposes.

Parts of the project were developed while following external educational material. The repository represents my own working implementation, experimentation, configuration, and extensions developed during the learning process.
