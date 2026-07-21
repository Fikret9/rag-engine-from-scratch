import os
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

from DocumentMetadataStore import DocumentMetadataStore

from RAGChatbot import RAGChatbot
from chunker import Chunker
from evaluate import evaluate
from ollama_embedding_provider import OllamaEmbeddingProvider
from ollama_llm_provider import OllamaLLMProvider
from pdf_reader import PDFReader

from retriever import Retriever
from build_embeddings import build_embeddings
from test_cases import test_cases
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
QDRANT_PATH = PROJECT_ROOT / "qdrant_data"

client = QdrantClient(path=str(QDRANT_PATH))

try:
    metadata_store = DocumentMetadataStore()
    metadata_store.load()
    model_id = "nomic-embed-text"
    provider = OllamaEmbeddingProvider(model_id)
    all_chunks =[]
    all_embeddings = []

    existing = {c.name for c in client.get_collections().collections}

    if "documents" not in existing:
        client.create_collection(
        collection_name="documents",
        vectors_config=VectorParams(
        size=768,
        distance=Distance.COSINE,
        ),
        )

    for file_path in os.listdir("data"):
        full_path = os.path.join("data", file_path)
        filename = file_path
        sha256, last_modified = DocumentMetadataStore.compute_file_info(full_path)
        chunk_file = f"cache/chunks/{filename}.json"
        chunk_file = chunk_file.replace(".pdf", "")

        if filename not in metadata_store.data:
            extractor = PDFReader(full_path)
            doc = extractor.read()
            """    Create chunks """
            chunker = Chunker()
            chunks = chunker.chunk(doc)
            metadata_store.update_document(filename,sha256,last_modified)
            texts = [chunk.text for chunk in chunks]
            """    Create embeddings from Vectors """
            response = provider.embed(texts)
            embeddings = build_embeddings(chunks, response.embeddings, model_id) #"""    Build embeddings """

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

            client.upsert(
                    collection_name="documents",
                    points=points,
            )

            metadata_store.add_embedding_model(filename,model_id)
            metadata_store.save()
        elif metadata_store.has_changed(filename, sha256):
            print ("Store changed")
        else:
            print ("Store unchanged")

    """    Create Vector for the query """
    response = provider.embed([" vacation policy"])
    question_vector = response.embeddings[0]

    """    Retrieve top results """
    retriever = Retriever(client)
    #retriever.delete_document(r"data\jayabraham.pdf")
    results = retriever.find_relevant_context(question_vector)
    print("------------------------------------------------------------")
    print(results)

    """    Test a batch """
    evaluate(test_cases, provider,retriever)

    """    Ask LLM """
    chat_model="qwen2.5:1.5b"
    llm_provider = OllamaLLMProvider(chat_model)
    bot = RAGChatbot(provider=provider, retriever=retriever, llm_provider=llm_provider, client=client)
    bot.chat_loop()
finally:
    client.close()