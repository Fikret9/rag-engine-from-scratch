import json
import os
import hashlib
from dataclasses import asdict


class RecordStore:
    def __init__(self, model_class, file_path):
        self.model_class = model_class
        self.file_path = file_path

    def exists(self):
        return os.path.exists(self.file_path)

    def load(self):
        with open(self.file_path) as f:
            data = json.load(f)
            records = [self.model_class(**item) for item in data]
        return records

    def save(self,data):
        data = [asdict(item) for item in data]
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def compute_file_info(file_path):
        with open(file_path, "rb") as f:
            content = f.read()
        sha256 = hashlib.sha256(content).hexdigest()
        last_modified = os.path.getmtime(file_path)
        return sha256, last_modified

    def has_changed(self, filename, new_sha256):
        if filename not in self.data:
            return True
        else:
            return self.data[filename]["sha256"] != new_sha256

    def update_document(self, filename, sha256, last_modified):
        self.data[filename] = {"sha256": sha256, "last_modified": last_modified, "embeddings": []}

    def add_embedding_model(self, filename, model_id):
        models = self.data[filename]["embeddings"]
        if model_id not in models:
            models.append(model_id)

    def has_embedding(self, filename, model_id):
        models = self.data[filename]["embeddings"]
        return model_id in models