# Module 3 — Support Assistant

## Overview

This module builds a GenAI support assistant for Zepto. It uses Zepto policy documents as its knowledge base and answers policy-related questions using a RAG (Retrieval-Augmented Generation) pipeline.

The main flow is:

**Documents → Embeddings → ChromaDB → Retrieval → LangGraph → Answer → FastAPI**

The module works in a fully offline **mock mode**, which is the required graded mode.

## Technologies

* Python
* LangGraph
* ChromaDB
* Sentence Transformers
* FastAPI
* Pydantic
* Uvicorn
* Docker

## Document Corpus

The project contains 8 Zepto policy documents in the `docs/` folder:

```text
docs/
├── doc_01.txt
├── doc_02.txt
├── doc_03.txt
├── doc_04.txt
├── doc_05.txt
├── doc_06.txt
├── doc_07.txt
└── doc_08.txt
```

The documents cover:

* Delivery
* Returns and refunds
* Membership
* Order tracking
* Order cancellation
* Damaged or missing items
* Gift cards
* Customer support hours

## RAG Pipeline

### 1. Ingestion

The application loads all 8 policy documents and divides them into chunks.

### 2. Embeddings

Each chunk is converted into an embedding using:

```text
all-MiniLM-L6-v2
```

from Sentence Transformers.

The embeddings are stored in ChromaDB.

### 3. Retrieval

When a policy question is received, the system searches ChromaDB and retrieves the **top 3 most similar chunks** using cosine similarity.

### 4. Generation

The retrieved information is used to generate the answer.

In the required mock mode, no external LLM is called. The answer is generated using the most relevant retrieved chunk.

## LangGraph

The application uses a LangGraph `StateGraph` with three main nodes:

```text
classify_intent
       |
       ├── policy_question → retrieve_and_answer
       |
       └── general_question → direct_answer
```

### `classify_intent`

In mock mode, the query is classified using keywords.

The following keywords are treated as policy questions:

```text
delivery
return
refund
membership
tracking
cancel
gift card
support hours
```

### `retrieve_and_answer`

For policy questions, the system:

1. Embeds the query.
2. Searches ChromaDB.
3. Retrieves the top 3 chunks.
4. Uses the most relevant chunk to create the mock response.

Example:

```text
Based on the retrieved context: <retrieved text>
```

### `direct_answer`

For general questions, the mock system returns:

```text
I can only answer questions about Zepto policies right now.
```

## Mock LLM Mode

The application uses the `MOCK_LLM` environment variable.

The default required mode is:

```text
MOCK_LLM=1
```

or leaving the variable unset.

This mode does not require:

* An API key
* An LLM account
* Paid services
* Network access to an LLM

An optional real LLM can be enabled with:

```text
MOCK_LLM=0
```

This is not required for grading.

## Structured Output

The final response is validated using Pydantic.

The response contains:

```json
{
  "answer": "Answer text",
  "sources": ["doc_01"],
  "confidence": 1.0
}
```

Where:

* `answer` contains the response.
* `sources` contains the retrieved document/chunk IDs.
* `confidence` is a value between `0` and `1`.

For general questions, `sources` is empty.

## FastAPI

The LangGraph application is exposed through a FastAPI endpoint:

```text
POST /ask
```

Example request:

```json
{
  "query": "How long does Zepto delivery take?"
}
```

Example policy-question flow:

```text
Query
 ↓
classify_intent
 ↓
policy_question
 ↓
retrieve_and_answer
 ↓
ChromaDB
 ↓
Answer
```

Example general-question flow:

```text
Query
 ↓
classify_intent
 ↓
general_question
 ↓
direct_answer
```

## Running the Application

Go to the module:

```bash
cd support_assistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn main:app --reload
```

The application can then be tested using the `/ask` endpoint.

## Docker

A Dockerfile is included for running the FastAPI application.

Build the image:

```bash
docker build -t zepto-support-assistant .
```

Run the container:

```bash
docker run -p 7860:7860 zepto-support-assistant
```

The API will be available through:

```text
POST /ask
```

## Architecture

```text
Zepto Policy Documents
        ↓
     Chunking
        ↓
   Embeddings
        ↓
    ChromaDB
        ↓
    User Query
        ↓
 classify_intent
      /   \
     /     \
Policy    General
  ↓          ↓
Retrieve   Direct
  ↓        Answer
  └────┬─────┘
       ↓
   Pydantic
       ↓
    FastAPI
```

The `MOCK_LLM` setting only changes the generation/classification logic. Document embedding and ChromaDB retrieval continue to work normally in both modes.

## Module Checklist

* [ ] 8 policy documents added.
* [ ] Documents embedded using `all-MiniLM-L6-v2`.
* [ ] ChromaDB collection created.
* [ ] LangGraph `StateGraph` implemented.
* [ ] Three required nodes implemented.
* [ ] Conditional routing implemented.
* [ ] Mock LLM mode implemented.
* [ ] Pydantic response schema implemented.
* [ ] FastAPI `/ask` endpoint implemented.
* [ ] Two example API calls documented.
* [ ] Dockerfile added and tested.
* [ ] RAG architecture documented.
