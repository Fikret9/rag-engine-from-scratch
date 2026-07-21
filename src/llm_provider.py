from abc import ABC, abstractmethod

class LLMProvider(ABC):
    def __init__(self, model_id: str):
        self.model_id = model_id

    @abstractmethod
    def generate(self, prompt: str):
        pass