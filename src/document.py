from dataclasses import dataclass

@dataclass
class Document:
    text: str
    source: str
    page_count: int
