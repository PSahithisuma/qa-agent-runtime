from qdrant_client import QdrantClient


class VectorService:

    def __init__(self):

        try:

            self.client = QdrantClient(
                host="localhost",
                port=6333,
                timeout=5
            )

            self.enabled = True

        except Exception:

            self.enabled = False

    def is_ready(self):

        return self.enabled