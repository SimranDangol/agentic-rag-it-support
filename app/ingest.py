import glob
import json
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec

from app import config


def main():
    splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
    chunks = []

    for path in sorted(glob.glob("data/kb/*.md")):
        name = os.path.basename(path)
        text = open(path, encoding="utf-8").read()
        for i, part in enumerate(splitter.split_text(text)):
            chunks.append({"id": f"{name}-{i}", "source": name, "text": part})

    model = SentenceTransformer(config.EMBED_MODEL)
    vectors = model.encode([c["text"] for c in chunks], show_progress_bar=True)

    pc = Pinecone(api_key=config.PINECONE_API_KEY)
    if config.INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=config.INDEX_NAME,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    index = pc.Index(config.INDEX_NAME)

    batch = []
    for c, v in zip(chunks, vectors):
        batch.append(
            {
                "id": c["id"],
                "values": v.tolist(),
                "metadata": {"source": c["source"], "text": c["text"]},
            }
        )
        if len(batch) == 100:
            index.upsert(vectors=batch)
            batch = []
    if batch:
        index.upsert(vectors=batch)

    json.dump(chunks, open("data/chunks.json", "w", encoding="utf-8"))
    print(
        f"Indexed {len(chunks)} chunks from "
        f"{len(set(c['source'] for c in chunks))} files"
    )


if __name__ == "__main__":
    main()
