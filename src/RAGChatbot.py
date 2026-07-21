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

        parts = []


        for score, text, source in results:
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
        
        Context:
        {context_text}
        Question:
        {question}
        If the answer is not in the context, say you don't know.
        """

        return self.llm_provider.generate(prompt)


    def chat_loop(self):
        while True:
            question = input("Enter your question (or type 'quit'): ").strip()
            if question.lower() == "quit":
                break
            print(self.ask(question))

    def ask_clicked():

        question = question_entry.get()
        answer = chatbot.ask(question)
        response_box.delete("1.0", "end")
        response_box.insert("end", answer)