from dataclasses import dataclass

@dataclass
class Embedding:
    chunk_id: int
    model_id: str
    vector: list[float]