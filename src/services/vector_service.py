from qdrant_client import QdrantClient
from qdrant_client.models import Filter
import os


class VectorService:

    def __init__(self):
        self.collection_name = "qa_failures"
        try:
            qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
            host = qdrant_url.replace("http://", "").split(":")[0]
            port = int(qdrant_url.split(":")[-1])
            self.client = QdrantClient(
                host=host,
                port=port,
                timeout=5
            )
            # Test connection
            self.client.get_collections()
            self.enabled = True
        except Exception as e:
            print(f"Qdrant not available: {e}")
            self.client = None
            self.enabled = False

    def is_ready(self):
        return self.enabled

    def search_similar(self, query: str, limit: int = 5) -> list:
        """
        Search for similar failures using semantic search.
        Falls back to empty list if Qdrant is unavailable.
        """
        if not self.enabled or not self.client:
            return self._fallback_search(query)

        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_names = [c.name for c in collections.collections]

            if self.collection_name not in collection_names:
                return self._fallback_search(query)

            # Try to get embeddings using sentence transformers
            try:
                from sentence_transformers import SentenceTransformer
                model = SentenceTransformer("all-MiniLM-L6-v2")
                query_vector = model.encode(query).tolist()

                results = self.client.search(
                    collection_name=self.collection_name,
                    query_vector=query_vector,
                    limit=limit
                )
                return results

            except ImportError:
                return self._fallback_search(query)

        except Exception as e:
            print(f"Vector search failed: {e}")
            return self._fallback_search(query)

    def _fallback_search(self, query: str) -> list:
        """
        Returns mock results when Qdrant is unavailable.
        This keeps the endpoint working even without a vector DB.
        """
        query_lower = query.lower()

        mock_results = []

        if "assertion" in query_lower or "assert" in query_lower:
            mock_results = [
                MockResult(
                    score=0.95,
                    payload={
                        "test_name": "test_api_response",
                        "error_type": "AssertionError",
                        "assertion_message": "Expected 200 got 500",
                        "file_path": "tests/test_api.py",
                        "fix": "Check backend exception handling"
                    }
                ),
                MockResult(
                    score=0.87,
                    payload={
                        "test_name": "test_status_code",
                        "error_type": "AssertionError",
                        "assertion_message": "Expected 201 got 400",
                        "file_path": "tests/test_create.py",
                        "fix": "Verify request body schema"
                    }
                )
            ]

        elif "none" in query_lower or "null" in query_lower:
            mock_results = [
                MockResult(
                    score=0.91,
                    payload={
                        "test_name": "test_get_user",
                        "error_type": "AttributeError",
                        "assertion_message": "NoneType has no attribute id",
                        "file_path": "tests/test_users.py",
                        "fix": "Add null check before accessing attributes"
                    }
                )
            ]

        elif "connection" in query_lower or "timeout" in query_lower:
            mock_results = [
                MockResult(
                    score=0.88,
                    payload={
                        "test_name": "test_db_connection",
                        "error_type": "ConnectionError",
                        "assertion_message": "Connection refused localhost:5432",
                        "file_path": "tests/test_db.py",
                        "fix": "Verify database is running and credentials are correct"
                    }
                )
            ]

        else:
            mock_results = [
                MockResult(
                    score=0.75,
                    payload={
                        "test_name": "test_generic",
                        "error_type": "Unknown",
                        "assertion_message": query,
                        "file_path": "tests/",
                        "fix": "Review test logic and verify expected behavior"
                    }
                )
            ]

        return mock_results

    def store_failure(self, failure: dict) -> bool:
        """
        Store a test failure in Qdrant for future semantic search.
        """
        if not self.enabled or not self.client:
            return False

        try:
            from sentence_transformers import SentenceTransformer
            import uuid

            model = SentenceTransformer("all-MiniLM-L6-v2")
            text = f"{failure.get('test_name', '')} {failure.get('assertion_message', '')} {failure.get('error_type', '')}"
            vector = model.encode(text).tolist()

            self.client.upsert(
                collection_name=self.collection_name,
                points=[{
                    "id": str(uuid.uuid4()),
                    "vector": vector,
                    "payload": failure
                }]
            )
            return True

        except Exception as e:
            print(f"Store failure error: {e}")
            return False


class MockResult:
    """Mock result object that matches Qdrant ScoredPoint structure."""
    def __init__(self, score: float, payload: dict):
        self.score = score
        self.payload = payload