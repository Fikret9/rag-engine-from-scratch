
import ollama
import embedding
import time

from embedding_provider import EmbeddingProvider


class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model_id: str = "nomic-embed-text"):
        super().__init__(model_id=model_id)

    def embed(self, chunks) -> list[embedding.Embedding]:
        if not chunks:
            return []
        start = time.perf_counter()

        response = ollama.embed(model=self.model_id, input=[chunk for chunk in chunks])

        end = time.perf_counter()
        elapsed = end - start
        print(f"Embed duration Elapsed: {elapsed:.3f} seconds")

        return response