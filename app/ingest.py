import json
import time
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app import config


PROJECT_ROOT = Path(__file__).resolve().parents[1]
KB_DIR = PROJECT_ROOT / "data" / "kb"
CHUNKS_PATH = PROJECT_ROOT / "data" / "chunks.json"
UPSERT_BATCH_SIZE = 100


def build_chunks(kb_dir: Path = KB_DIR) -> list[dict[str, str]]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
    chunks = []

    for path in sorted(kb_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for i, part in enumerate(splitter.split_text(text)):
            chunks.append(
                {"id": f"{path.name}-{i}", "source": path.name, "text": part}
            )

    return chunks


def main() -> None:
    if not config.PINECONE_API_KEY.strip():
        raise RuntimeError(
            "PINECONE_API_KEY is not set. Add it to your environment or .env file "
            "before running ingestion."
        )

    chunks = build_chunks()
    if not chunks:
        raise FileNotFoundError(f"No Markdown knowledge-base documents found in {KB_DIR}")

    from pinecone import Pinecone, ServerlessSpec
    from sentence_transformers import SentenceTransformer

    print(f"Loading embedding model '{config.EMBED_MODEL}'...", flush=True)
    model = SentenceTransformer(config.EMBED_MODEL)
    print(f"Embedding {len(chunks)} chunks...", flush=True)
    vectors = model.encode([chunk["text"] for chunk in chunks], show_progress_bar=False)
    if len(vectors) != len(chunks):
        raise RuntimeError(
            f"Embedding count mismatch: received {len(vectors)} vectors "
            f"for {len(chunks)} chunks."
        )
    if any(len(vector) != config.EMBED_DIMENSION for vector in vectors):
        raise RuntimeError(
            "Embedding model output does not match Pinecone's "
            f"{config.EMBED_DIMENSION} dimensions."
        )

    print("Connecting to Pinecone...", flush=True)
    pinecone = Pinecone(api_key=config.PINECONE_API_KEY)
    existing_indexes = [idx.name for idx in pinecone.list_indexes()]
    if config.INDEX_NAME not in existing_indexes:
        print(f"Creating Pinecone index '{config.INDEX_NAME}'...", flush=True)
        pinecone.create_index(
            name=config.INDEX_NAME,
            dimension=config.EMBED_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        while not pinecone.describe_index(config.INDEX_NAME).status["ready"]:
            print("Waiting for Pinecone index to be ready...", flush=True)
            time.sleep(2)
        print("Pinecone index is ready.", flush=True)

    print(f"Opening index '{config.INDEX_NAME}'...", flush=True)
    index = pinecone.Index(config.INDEX_NAME)

    for start in range(0, len(chunks), UPSERT_BATCH_SIZE):
        batch_chunks = chunks[start : start + UPSERT_BATCH_SIZE]
        batch_vectors = vectors[start : start + UPSERT_BATCH_SIZE]
        print(
            f"Upserting batch {start + 1}..{start + len(batch_chunks)} of {len(chunks)}...",
            flush=True,
        )
        index.upsert(
            vectors=[
                {
                    "id": chunk["id"],
                    "values": vector.tolist(),
                    "metadata": {"source": chunk["source"], "text": chunk["text"]},
                }
                for chunk, vector in zip(batch_chunks, batch_vectors)
            ]
        )

    CHUNKS_PATH.write_text(
        json.dumps(chunks, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Successfully indexed {len(chunks)} chunks from {len({c['source'] for c in chunks})} files.",
        flush=True,
    )


if __name__ == "__main__":
    main()
