import os
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

from DocumentMetadataStore import DocumentMetadataStore

from RAGChatbot import RAGChatbot
from document_processor import DocumentProcessor
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

    processor = DocumentProcessor(
        client,
        provider,
        metadata_store,
        model_id
    )

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
        processor.process_document(full_path)
        print("here")

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

