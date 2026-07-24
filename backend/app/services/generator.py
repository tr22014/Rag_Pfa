import ollama


class Generator:
    def __init__(self, model: str = "qwen2.5:7b"):
        self.model = model

    def generate(self, question: str, context: str) -> str:

        prompt = f"""
                You are an AI assistant specialized in Retrieval-Augmented Generation (RAG).

                Answer ONLY using the information contained in the provided context.

                Rules:
                - Use ONLY the provided context.
                - Never use external knowledge.
                - Never invent facts.
                - If the answer is not present in the context, reply exactly:
                I don't know.
                - Detect the language of the user's question.
                - Answer in exactly the same language:
                    • English → English
                    • French → French
                    • Arabic → العربية
                - If the context contains information in another language, translate it into the user's language.
                - Be concise and accurate.
                - Merge relevant information from multiple context passages.
                - Do not mention the context.

                Context:
                {context}

                Question:
                {question}

                Answer:
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