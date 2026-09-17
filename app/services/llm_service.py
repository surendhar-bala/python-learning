import ollama


def generate_answer(question: str, context: str):
    prompt = f"""
You are a helpful assistant that answers questions based only on
the provided document context.

Document context:
{context}

Question:
{question}

Instructions:
- Answer using the provided context.
- If the answer is not present in the context, say:
  "I could not find the answer in the document."
- Do not make up information.

Answer:
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]