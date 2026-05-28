import os
import chromadb
from chromadb.utils import embedding_functions

DOCS_PATH = "sample_docs"
KB_PATH = "knowledge_base"

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

def chunk_text(text, chunk_size=200, overlap=40):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def ingest_domain(domain):
    print(f"\nIngesting [{domain}] knowledge base...")
    client = chromadb.PersistentClient(path=f"{KB_PATH}/{domain}")
    try:
        client.delete_collection(domain)
    except Exception:
        pass
    collection = client.create_collection(
        name=domain, embedding_function=embedding_fn
    )
    docs_dir = f"{DOCS_PATH}/{domain}"
    all_chunks, all_ids, all_metadata = [], [], []
    chunk_id = 0
    for filename in sorted(os.listdir(docs_dir)):
        if filename.endswith((".txt", ".pdf")):
            filepath = os.path.join(docs_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            chunks = chunk_text(text)
            for chunk in chunks:
                all_chunks.append(chunk)
                all_ids.append(f"{domain}_{chunk_id}")
                all_metadata.append({"source": filename, "domain": domain})
                chunk_id += 1
            print(f"  {filename} -> {len(chunks)} chunks")
    if all_chunks:
        collection.add(documents=all_chunks, ids=all_ids, metadatas=all_metadata)
        print(f"  Stored {len(all_chunks)} total chunks in [{domain}] vector store")

if __name__ == "__main__":
    print("=" * 50)
    print("Multi-Agent RAG - Knowledge Base Ingestion")
    print("=" * 50)
    for domain in ["finance", "research", "legal"]:
        ingest_domain(domain)
    print("\nAll knowledge bases ready.")
