from pathlib import Path

from pdf_reader import PDFReader
from text_reader import TextReader
from word_reader import WordReader


class DocumentReaderFactory:

    @staticmethod
    def create(filename):

        ext = Path(filename).suffix.lower()

        if ext == ".pdf":
            return PDFReader(filename)

        if ext == ".docx":
            return WordReader(filename)

        if ext == ".txt":
            return TextReader(filename)

        raise ValueError(f"Unsupported document type: {ext}")