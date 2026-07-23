import ollama


class Generator:
    def __init__(self, model: str = "llama3.2"):
        self.model = model

    def generate(self, question: str, context: str) -> str:

        prompt = f"""
            You are an AI assistant specialized in document question answering.

            Your task is to answer questions ONLY using the provided context.

            Rules:

            - Use ONLY the information contained in the context.
            - NEVER use your own knowledge.
            - NEVER invent information.
            - If the answer cannot be found in the context, answer exactly:
            "I don't know."
            - Answer in the SAME language as the user's question.
            - Keep the answer concise but complete.
            - If several context passages contain useful information, combine them into one coherent answer.
            - Do not mention that you are using a context.
            - Do not quote the entire context unless explicitly requested.

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