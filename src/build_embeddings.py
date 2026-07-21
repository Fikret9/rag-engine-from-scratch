import embedding


def build_embeddings(chunks, vectors, model_id):
    return [
        embedding.Embedding(
            chunk_id=chunk.id,
            model_id=model_id,
            vector=vec,
        )
        for chunk, vec in zip(chunks, vectors)
    ]