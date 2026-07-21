import os
from pathlib import Path

from qdrant_client import QdrantClient
import pydantic

#print("Qdrant:", qdrant_client.__version__)
print("Pydantic:", pydantic.__version__)
print(os.getcwd())

PROJECT_ROOT = Path(__file__).resolve().parent.parent
QDRANT_PATH = PROJECT_ROOT / "qdrant_data"

client = QdrantClient(path=str(QDRANT_PATH))
help(client.d)

collections = client.get_collections()
print(collections)

try:
    print(client)
finally:
    client.close()