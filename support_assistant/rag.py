from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# Paths
BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "docs"
CHROMA_DIR = BASE_DIR / "chroma_db"


# Embedding model required by the capstone
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


def load_documents():
    """Load all policy documents from the docs folder."""

    documents = []

    for file_path in sorted(DOCS_DIR.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8").strip()

        documents.append(
            {
                "id": file_path.stem,
                "text": text,
            }
        )

    return documents


def create_vector_store():
    """Create the ChromaDB collection and store document embeddings."""

    documents = load_documents()

    print(f"Loaded {len(documents)} documents.")

    # Load the local embedding model
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    # Persistent ChromaDB client
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Create or get our collection
    collection = client.get_or_create_collection(
        name="zepto_policies",
        configuration={"hnsw": {"space": "cosine"}},
    )

    # Add each document
    for document in documents:
        embedding = model.encode(document["text"]).tolist()

        collection.upsert(
            ids=[document["id"]],
            documents=[document["text"]],
            embeddings=[embedding],
            metadatas=[
                {
                    "document_id": document["id"],
                }
            ],
        )

        print(f"Added: {document['id']}")

    print(f"\nChromaDB collection contains {collection.count()} documents.")

    return collection


def retrieve_documents(query, top_k=3):
    """Retrieve the most relevant policy documents for a query."""

    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    collection = client.get_collection(
        name="zepto_policies"
    )

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    return results


if __name__ == "__main__":

    create_vector_store()

    results = retrieve_documents(
        "What is the delivery fee?"
    )

    print("\nRetrieved documents:")

    for document_id, document in zip(
        results["ids"][0],
        results["documents"][0],
    ):
        print(f"\nID: {document_id}")
        print(f"Content: {document[:200]}...")