from abc import ABC, abstractmethod

class DocumentReader(ABC):

    @abstractmethod
    def read(self, filename: str) -> str:
        pass