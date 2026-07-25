class RAGChatbot:
    def __init__(self, provider, retriever, llm_provider, client):
        self.provider = provider
        self.retriever = retriever
        self.llm_provider = llm_provider
        self.client = client

    def ask(self, question):
        response = self.provider.embed([question])
        question_vector = response.embeddings[0]
        results = self.retriever.find_relevant_context(question_vector)

        for r in results:
            print(r)

        parts = []
        for score, text, source in results:
            print(score, source)
            parts.append(
                f"Source: {source}\n{text}"
            )

        context_text = "\n\n---\n\n".join(parts)

        prompt = f"""
        You are answering questions about company documents.
        Answer using only the provided context.

        If the context contains only part of the answer,
        answer with whatever information is available.

        Only say "I don't know" if the context contains
        no relevant information.
        
        Do not include document names or source citations in your answer.
        The UI displays sources separately.
        
        Context:
        {context_text}
        Question:
        {question}
        If the answer is not in the context, say you don't know.
        """

        answer = self.llm_provider.generate(prompt)
        return answer, results      # <-- CHANGED


    def chat_loop(self):
        while True:
            question = input("Enter your question (or type 'quit'): ").strip()
            if question.lower() == "quit":
                break
            print(self.ask(question))
