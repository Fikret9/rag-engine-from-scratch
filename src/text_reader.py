from DocumentReader import DocumentReader
from document import Document


class TextReader(DocumentReader):
    def __init__(self, file_path: str):
        self.file_path = file_path


    def read(self):
        with open(self.file_path, encoding="utf-8") as f:
         return Document(
                text=f.read(),
                source=self.file_path
             )