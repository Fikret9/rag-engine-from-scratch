from qdrant_client.models import Filter, FieldCondition, MatchValue

class Retriever:
    def __init__(self,  client):
        self.client = client
        """
        Takes a user query embedding, calculates cosine similarity against
        stored records, and returns the top K most relevant text chunks.
        """

    def find_relevant_context(self, question_embedding, top_k: int = 3):

        if not question_embedding:
            return []

        response = self.client.query_points( collection_name="documents",
                                  query=question_embedding,
                                  limit=top_k,
                                  with_payload=True)

        #print(response)

        results = []
        for point in response.points:
            print(f"Score: {point.score:.3f}")

            results.append(
                (
                    point.score,
                    point.payload["text"],
                    point.payload["source"],
                )
            )

        for score, text, source in results:
            print(repr(source))

        return results


    def delete_document(self, source: str) -> None:

        response = self.client.scroll(
                collection_name="documents",
                scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="source",
                        match=MatchValue(value="data\\jayabraham.pdf")
                    )
                ]
            ),
            limit=10,
        )
        print(response)

        print(f"DELETING{source}")

        self.client.delete(
            collection_name="documents",
            points_selector=Filter(
            must=[
                FieldCondition(
                    key="source",
                    match=MatchValue(value=source),
                )
            ]
        ),
    )

