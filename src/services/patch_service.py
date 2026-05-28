import requests
import os


class PatchService:

    def __init__(self):
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3")

    def generate_patch(self, failure: dict) -> str:
        assertion = failure.get("assertion_message", "")
        error_type = failure.get("error_type", "")
        test_name = failure.get("test_name", "")
        file_path = failure.get("file_path", "")
        stack_trace = failure.get("stack_trace", "")

        ai = self._get_ai_suggestion(assertion, error_type, test_name, file_path, stack_trace)
        if ai:
            return ai
        return self._rule_based_suggestion(assertion, error_type)

    def _get_ai_suggestion(self, assertion, error_type, test_name, file_path, stack_trace=""):
        try:
            prompt = (
                f"You are an expert software engineer helping fix failing tests.\n\n"
                f"Test name: {test_name}\n"
                f"File: {file_path}\n"
                f"Error type: {error_type}\n"
                f"Assertion: {assertion}\n"
                f"Stack trace: {stack_trace}\n\n"
                f"Provide: 1) Root cause 2) Fix suggestion 3) Code example"
            )
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.3, "num_predict": 300}
                },
                timeout=30
            )
            if response.status_code == 200:
                suggestion = response.json().get("response", "").strip()
                if suggestion:
                    return suggestion
            return None
        except Exception:
            return None

    def _rule_based_suggestion(self, assertion, error_type):
        a = assertion.lower()
        if "500" in assertion:
            return "Root cause: Server 500 error.\nFix: Check backend exception handling and verify API returns HTTP 200 for valid requests."
        if "404" in assertion:
            return "Root cause: Endpoint not found.\nFix: Verify URL path is correct and route is registered in the router."
        if "401" in assertion or "403" in assertion:
            return "Root cause: Auth failure.\nFix: Check auth token is correct and not expired. Verify user has required role."
        if "422" in assertion:
            return "Root cause: Request validation failed.\nFix: Check request body matches schema. Verify all required fields are present."
        if "nonetype" in a:
            return "Root cause: Object is None.\nFix: Add null check before accessing attributes. Example: if obj is not None: obj.attribute"
        if "connection refused" in a:
            return "Root cause: Service connection refused.\nFix: Verify service is running. Check host/port in environment variables."
        if "timeout" in a:
            return "Root cause: Request timed out.\nFix: Increase timeout values. Check service health and optimize slow queries."
        if "assert" in a:
            return "Root cause: Assertion failed - actual value does not match expected.\nFix: Print actual response to debug. Verify test data is correct."
        if "keyerror" in a:
            return "Root cause: Key not found in response.\nFix: Print full response body to check available keys."
        if "typeerror" in a:
            return "Root cause: Wrong data type.\nFix: Check data types in function signature and API response."
        return f"Root cause: {error_type}.\nFix: Review the failing assertion and validate expected behavior."

    def generate_batch_patches(self, failures: list) -> list:
        results = []
        for failure in failures:
            suggestion = self.generate_patch(failure)
            results.append({
                "test_name": failure.get("test_name", "unknown"),
                "file_path": failure.get("file_path", ""),
                "error_type": failure.get("error_type", ""),
                "patch_suggestion": suggestion
            })
        return results

    def is_ollama_available(self) -> bool:
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return any(self.model in m.get("name", "") for m in models)
            return False
        except Exception:
            return False