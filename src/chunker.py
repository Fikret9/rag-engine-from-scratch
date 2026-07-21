import os

import document
from chunk import Chunk
from document import Document

class Chunker:

    def chunk(self, document: Document) -> list[Chunk]:
        chunk_size = 200
        overlap = 0
        words = document.text.split()
        step = chunk_size - overlap
        chunks = []
        chunk_id=0
        for i in range(0, len(words), step):
            word_window = words[i : i + chunk_size]
            clean_chunk = " ".join(word_window)
            document_name = os.path.splitext(os.path.basename(document.source))[0]
            chunk_key = f"{document_name}:{chunk_id}"

            chunks.append(Chunk(
                id=chunk_key,
                text=clean_chunk,
                source=document.source,
                word_offset=i
            ))

            if i + chunk_size >= len(words):
                break
            chunk_id +=1

        print(f"Sanitization complete. Created {len(chunks)} text chunks.")
        return chunks
