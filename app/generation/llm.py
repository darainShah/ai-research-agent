import os
import ollama


class LLM:
    def __init__(self, model: str | None = None):
        self.model = model or os.getenv("OLLAMA_MODEL", "qwen3:4b")
        self.client = ollama.Client(
            host=os.getenv(
                "OLLAMA_URL",
                "http://host.docker.internal:11434"
            )
        )

    def rewrite_question(self, question: str, chat_history: list):
        """
        Rewrite a follow-up question into a standalone search query.

        If there is no conversation history, return the original question.
        """

        if not chat_history:
            return question

        history_text = "\n".join(
            [
                f"{message['role']}: {message['content']}"
                for message in chat_history[-6:]
            ]
        )

        prompt = f"""
You are a search-query rewriting system.

Your ONLY task is to rewrite the latest user question
into a standalone question that can be used for document search.

Use the conversation history to understand what the user is referring to.

IMPORTANT RULES:

1. Do NOT answer the question.

2. Do NOT explain your reasoning.

3. Return ONLY the rewritten standalone question.

4. Preserve the original meaning of the user's question.

5. Resolve references such as:
   - it
   - this
   - that
   - they
   - them
   - he
   - she
   - this method
   - this process
   - the above

6. Use the previous conversation to replace those references
with the actual topic.

7. Do NOT add facts that are not present in the conversation.

8. If the latest question is already standalone,
return it unchanged.

EXAMPLE:

Conversation:
user: What is AQI?
assistant: AQI is an indicator used to communicate air quality.

Latest question:
How is it calculated?

Correct output:
How is AQI calculated?

ANOTHER EXAMPLE:

Conversation:
user: What is token embedding?
assistant: Token embedding converts tokens into numerical vectors.

Latest question:
Why is it important?

Correct output:
Why is token embedding important?

Conversation history:
{history_text}

Latest user question:
{question}

Standalone search question:
"""

        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                think=False,
                options={
                    "temperature": 0,
                    "num_predict": 64
                }
            )

            rewritten_question = response["message"]["content"].strip()

            # Remove accidental labels sometimes produced by the model.
            prefixes = [
                "Standalone search question:",
                "Rewritten question:",
                "Standalone question:"
            ]

            for prefix in prefixes:
                if rewritten_question.lower().startswith(prefix.lower()):
                    rewritten_question = rewritten_question[
                        len(prefix):
                    ].strip()

            # Safety fallback.
            if not rewritten_question:
                return question

            return rewritten_question

        except Exception:
            # If rewriting fails, continue with the original question.
            return question

    def generate(
        self,
        question: str,
        context: str,
        chat_history: list = None
    ):
        """
        Generate an answer using only the retrieved document context.
        """

        if chat_history is None:
            chat_history = []

        history_text = "\n".join(
            [
                f"{message['role']}: {message['content']}"
                for message in chat_history[-6:]
            ]
        )
        prompt = f"""
You answer questions using ONLY the document sources below.

RULES:
- Answer the user's question directly.
- Do NOT show your reasoning.
- Do NOT say "I need to", "let me analyze", "let me see", or similar.
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



        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            think=False,
            options={
                "temperature": 0,
                "num_predict": 512
            }
        )

        return response["message"]["content"].strip()