import ollama


class Generator:

    def __init__(self, model: str = "qwen2.5:7b"):
        self.model = model


    def generate(
        self,
        question: str,
        context: str,
        history: list = None
    ) -> str:


        # Transformer l'historique en texte
        conversation_history = ""

        if history:

            for message in history:

                conversation_history += (
                    f"{message['role']}: "
                    f"{message['content']}\n"
                )


        prompt = f"""
You are an AI assistant specialized in Retrieval-Augmented Generation (RAG).

Answer ONLY using the provided context.

Rules:
- Use ONLY the provided context.
- Never use external knowledge.
- Never invent facts.
- If the answer is not present in the context, reply exactly:
I don't know.

Conversation history:
{conversation_history}


Relevant documents:
{context}


Current question:
{question}


Instructions:
- Use the conversation history only to understand references like:
  "it", "this", "these", "his", "their", "ses", "son", "ce".
- The final answer must still be based ONLY on the provided documents.
- Detect the language of the user's question.
- Answer in exactly the same language:
    • English → English
    • French → French
    • Arabic → العربية
- If the context contains information in another language, translate it.
- Be concise and accurate.
- Do not mention the conversation history.
- Do not mention the documents.

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