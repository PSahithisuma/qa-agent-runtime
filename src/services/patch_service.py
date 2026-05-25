import requests


class PatchService:

    def __init__(self):

        self.ollama_url = (
            "http://localhost:11434/api/generate"
        )

        self.model = "llama3"

    def generate_patch(

        self,

        failure: dict
    ):

        prompt = f"""
Fix Python test failure.

Assertion:
{failure.get("assertion_message")}

Give short fix only.
"""

        try:

            response = requests.post(

                self.ollama_url,

                json={

                    "model": self.model,

                    "prompt": prompt,

                    "stream": False,

                    "options": {

                        "num_predict": 120,

                        "temperature": 0.2
                    }
                },

                timeout=300
            )

            response.raise_for_status()

            data = response.json()

            return data.get(
                "response",
                "No patch generated"
            )

        except Exception as e:

            return (

                "Patch generation failed: "

                f"{str(e)}"
            )