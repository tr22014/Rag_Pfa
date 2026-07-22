import ollama


class Generator:
    def __init__(self, model: str = "llama3.2"):
        self.model = model

    def generate(self, question: str, context: str) -> str:

        prompt = f"""
You are an AI assistant specialized in document question answering.

Rules:
- Answer ONLY using the provided context.
- Do NOT use your own knowledge.
- If the answer is not present in the context, answer exactly:
  "I don't know."
- Answer in the SAME language as the user's question.
- Be concise but complete.
- If appropriate, summarize instead of copying the context verbatim.

====================
CONTEXT
====================

{context}

====================
QUESTION
====================

{question}

====================
ANSWER
====================
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]