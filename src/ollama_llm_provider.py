import ollama
import time

from llm_provider import LLMProvider


class OllamaLLMProvider(LLMProvider):
    def __init__(self, model_id: str = "qwen2.5:1.5b"):
        super().__init__(model_id=model_id)

    def generate(self, prompt) -> str:
        if not prompt:
            return ""

        start = time.perf_counter()

        response = ollama.chat(
            model=self.model_id,
            messages=[{"role": "user", "content": prompt}]
        )

        end = time.perf_counter()
        elapsed = end - start
        print(f"llm duration Elapsed: {elapsed:.3f} seconds")

        return response["message"]["content"]