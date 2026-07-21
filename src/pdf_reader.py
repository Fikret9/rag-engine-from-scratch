from pypdf import PdfReader

import document
from document import Document


class PDFReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self) -> Document:
        reader = PdfReader(self.file_path)
        # Create an empty list to hold the text from each page
        all_pages_text = []
        page_count=0
    # 1. Loop through the PDF page by page
        for page in reader.pages:
            page_count += 1
            page_text = page.extract_text()
        # 2. If the page actually has text (isn't blank or an image), save it
            if page_text:
                all_pages_text.append(page_text)
    # 3. Glue all the saved pages together with a newline in between
        print(f"source: {self.file_path} .. {page_count} pages")
        return Document(
            text="\n".join(all_pages_text),
            source=self.file_path,
            page_count=page_count
        )
