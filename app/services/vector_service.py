import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="pdf_documents"
)


def store_embeddings(
    chunks: list[str],
    embeddings: list[list[float]],
    filename: str
):
    ids = [
        f"{filename}_chunk_{index}"
        for index in range(len(chunks))
    ]

    metadatas = [
        {
            "filename": filename,
            "chunk_index": index
        }
        for index in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(ids)