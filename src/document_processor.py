import os
import uuid

from qdrant_client.grpc import PointStruct

from DocumentMetadataStore import DocumentMetadataStore
from build_embeddings import build_embeddings
from chunker import Chunker
from pdf_reader import PDFReader


class DocumentProcessor:

    def __init__(self, client, provider, metadata_store, model_id):
        self.client = client
        self.provider = provider
        self.metadata_store = metadata_store
        self.model_id = model_id

    def process_document(self,full_path):
        filename = os.path.basename(full_path)
        sha256, last_modified = DocumentMetadataStore.compute_file_info(full_path)
        chunk_file = f"cache/chunks/{filename}.json"
        chunk_file = chunk_file.replace(".pdf", "")

        if filename not in self.metadata_store.data:
            extractor = PDFReader(full_path)
            doc = extractor.read()
            """    Create chunks """
            chunker = Chunker()
            chunks = chunker.chunk(doc)
            self.metadata_store.update_document(filename,sha256,last_modified)
            texts = [chunk.text for chunk in chunks]
            """    Create embeddings from Vectors """
            response = self.provider.embed(texts)
            embeddings = build_embeddings(chunks, response.embeddings, self.model_id) #"""    Build embeddings """

            points = []
            for chunk, embedding in zip(chunks, embeddings):
                point_id = str(
                    uuid.uuid5(
                        uuid.NAMESPACE_URL,
                        chunk.id
                    )
                )
                points.append(

                    PointStruct(
                        id=point_id,
                        vector=embedding.vector,
                        payload={
                            "text": chunk.text,
                            "source": chunk.source,
                            "word_offset": chunk.word_offset,
                            "model_id": embedding.model_id,
                        },
                    )
                )

            self.client.upsert(
                collection_name="documents",
                points=points,
            )

            self.metadata_store.add_embedding_model(filename,self.model_id)
            self.metadata_store.save()
        elif self.metadata_store.has_changed(filename, sha256):
            print ("Store changed")
        else:
            print ("Store unchanged")



