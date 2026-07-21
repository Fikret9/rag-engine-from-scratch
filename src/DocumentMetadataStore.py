import hashlib
import json
import os


class DocumentMetadataStore:
    def __init__(self, file_path="metadata.json"):
        self.file_path = file_path
        if os.path.exists(self.file_path):
            with open(self.file_path) as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.data, f, indent=2)

    def load(self):
        if not os.path.exists(self.file_path):
            self.data = {}
            return

        with open(self.file_path) as f:
            self.data = json.load(f)

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