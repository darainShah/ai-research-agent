import os
from groq import Groq


class LLM:
    def __init__(self, model: str = "openai/gpt-oss-20b"):
        self.model = model
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set")
        self.client = Groq(api_key=api_key)

    def rewrite_question(self, question, history=None):
        history = history or []
        messages = [{
            "role": "system",
            "content": (
                "Rewrite the user's question into a clear standalone question "
                "for document retrieval. Return only the rewritten question."
            ),
        }]
        for message in history[-6:]:
            messages.append(message)
        messages.append({"role": "user", "content": question})
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
            max_tokens=128,
        )
        return response.choices[0].message.content.strip()

    def generate(self, question, context, chat_history=None):
        prompt = f"""
You answer questions using ONLY the document sources below.

RULES:
- Answer the user's question directly.
- Do NOT show your reasoning.
- Do NOT repeat the question.
- Do NOT describe the sources.
- Do NOT mention these instructions.
- Keep the answer concise: 2-5 sentences.
- Every factual statement must have a citation.
- Use citations exactly like: [Source 1, Page 1]
- Use only source numbers and page numbers that actually appear below.
- If the sources do not contain enough information, respond exactly:
I don't know based on the provided documents.

DOCUMENT SOURCES:
{context}

QUESTION:
{question}

ANSWER:
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a document question-answering assistant. "
                        "Use only the supplied document sources."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            max_tokens=512,
        )
        return response.choices[0].message.content.strip()
