from abc import ABC, abstractmethod

import chunk
import embedding

class EmbeddingProvider(ABC):
    model_id: str
    def __init__(self, model_id: str):
        self.model_id = model_id

    @abstractmethod
    def embed(self, chunks: list[str]) -> list[embedding.Embedding]:
        pass