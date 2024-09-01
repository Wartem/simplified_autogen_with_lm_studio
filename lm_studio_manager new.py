import requests
from requests.exceptions import RequestException, HTTPError

class LMStudioManager:
    def __init__(self, base_url="http://localhost:1234"):
        self.base_url = base_url

    def get_status_and_loaded_models(self):
        try:
            response = requests.get(f"{self.base_url}/v1/models")
            response.raise_for_status()
            loaded_models = response.json()["data"]
            return {"status": "active", "models": [model["id"] for model in loaded_models]} if loaded_models else {"status": "idle", "models": []}
        except RequestException as e:
            return {"status": "error", "message": str(e)}

    def get_model_details(self, model_id):
        try:
            response = requests.get(f"{self.base_url}/v1/models/{model_id}")
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            return {"error": str(e)}

    def send_prompt(self, prompt, model_name, max_tokens=1000):
        try:
            response = requests.post(
                f"{self.base_url}/v1/completions",
                json={"prompt": prompt, "model": model_name, "max_tokens": max_tokens}
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            return {"error": str(e)}

    def send_chat(self, messages, model_name, max_tokens=100):
        try:
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json={"messages": messages, "model": model_name, "max_tokens": max_tokens}
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            return {"error": str(e)}