from app.services.embedding_service import create_embeddings
from app.services.vector_service import collection
from app.services.llm_service import generate_answer


def search_documents(question: str, top_k: int = 5):
    question_embedding = create_embeddings([question])[0]

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    documents = results["documents"][0]

    print("\nQUESTION:")
    print(question)

    print("\nRETRIEVED DOCUMENTS:")
    for index, document in enumerate(documents):
        print(f"\n--- CHUNK {index} ---")
        print(document)

    context = "\n\n".join(documents)

    answer = generate_answer(
        question=question,
        context=context
    )

    return {
        "question": question,
        "answer": answer,
        "sources": documents
    }