import requests
import json
from requests.exceptions import RequestException, HTTPError


class LMStudioManager:
    def __init__(self, base_url="http://localhost:1234"):
        self.base_url = base_url

    def is_lm_studio_active(self):
        return self.get_status_and_loaded_models()["status"] == "active"

    def is_model_loaded(self, model):
        get_the_technical_name = lambda model: (
            model.split()[-1] if " " in model else model
        )
        model = get_the_technical_name(model)

        models_statuses = self.get_status_and_loaded_models()["models"]

        model_in_list = any(model in m for m in models_statuses)

        print("Model Status Requested:", model)
        print("Model loaded", models_statuses)
        print("Model found" if model_in_list else "Model was not found!")
        return model_in_list

    def get_loaded_models(self):
        return self.get_status_and_loaded_models()["models"]

    def get_status_and_loaded_models(self):
        """Check the status of loaded models in LM Studio."""
        try:
            response = requests.get(f"{self.base_url}/v1/models")
            response.raise_for_status()
            # print("Models loaded on the LM Studio server", response)
            loaded_models = response.json()["data"]
            # print("loaded models", loaded_models)
            if loaded_models:
                return {
                    "status": "active",
                    "models": [model["id"] for model in loaded_models],
                }
            else:
                return {"status": "idle", "models": []}
        except HTTPError as e:
            return {"status": "error", "message": f"HTTP error occurred: {e}"}
        except RequestException as e:
            return {"status": "error", "message": f"An error occurred: {e}"}

    """
    
    Below are methods that are not currently in use.
    These methods extend the capabilities of LMStudioManager for future use.
    
    """

    def list_available_models(self):
        """List all available models in LM Studio."""
        try:
            response = requests.get(f"{self.base_url}/v1/models")
            response.raise_for_status()
            return response.json()["data"]
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def send_prompt(self, prompt, model_name, max_tokens=1000):
        """Send a prompt to a specified model and get the response."""
        try:
            response = requests.post(
                f"{self.base_url}/v1/completions",
                json={"prompt": prompt, "model": model_name, "max_tokens": max_tokens},
            )
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            return {"error": f"HTTP error occurred: {e}"}
        except RequestException as e:
            return {"error": f"An error occurred: {e}"}

    def send_chat(self, messages, model_name, max_tokens=100):
        try:
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "messages": messages,
                    "model": model_name,
                    "max_tokens": max_tokens,
                },
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            return {"error": f"An error occurred: {e}"}

    def generate_embedding(self, input_text, model_name):
        try:
            response = requests.post(
                f"{self.base_url}/v1/embeddings",
                json={"input": input_text, "model": model_name},
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            return {"error": f"An error occurred: {e}"}

    def get_model_details(self, model_id):
        """Get detailed information about a specific model."""
        try:
            response = requests.get(f"{self.base_url}/v1/models/{model_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def save_config(self, config, filename="lm_studio_config.json"):
        """Save the current configuration to a JSON file."""
        with open(filename, "w") as f:
            json.dump(config, f, indent=4)

    def load_config(self, filename="lm_studio_config.json"):
        """Load configuration from a JSON file."""
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"error": "Configuration file not found"}
        except json.JSONDecodeError:
            return {"error": "Invalid JSON in configuration file"}

    def _print_model_details(self, model_name=None):
        """
        Prints detailed information about loaded models.

        :param model_name: Optional. The name or ID of a specific model to print details for.
        :return: A dictionary with 'success' (boolean) and 'message' (string) keys
        """
        # Get the list of loaded models
        loaded_models = self.get_status_and_loaded_models()

        if not loaded_models:
            return {"success": False, "message": "No models are currently loaded."}

        if model_name:
            # If a specific model is requested, check if it's loaded
            if model_name not in loaded_models:
                return {
                    "success": False,
                    "message": f"Error: Model '{model_name}' is not currently loaded.",
                }
            models_to_print = [model_name]
        else:
            # If no specific model is requested, print details for all loaded models
            models_to_print = loaded_models

        for model in models_to_print:
            # Get detailed information about the model
            model_info = self.get_model_details(model)

            if "error" in model_info:
                print(
                    f"Error retrieving details for model '{model}': {model_info['error']}"
                )
                continue

            # Print the details
            print(f"\nDetails for model: {model}")
            print("-" * 40)

            # Print each key-value pair in the model_info
            for key, value in model_info.items():
                print(f"{key.capitalize()}: {value}")

            print("-" * 40)

        return {"success": True, "message": "Model details printed successfully."}

    def _print_loaded_models(self, models):
        """
        Prints detailed information about all currently loaded models.
        """

        if models["status"] == "active" and (loaded_models := models["models"]):
            for model in loaded_models:
                # Get detailed information about the model
                print("Model:", model)
                model_details = self.get_model_details(model)

                print(f"\nDetails for model: {model}")
                print("-" * 40)

                if "error" in model_details:
                    print(f"Error retrieving model details: {model_details['error']}")
                else:
                    # Print each key-value pair in the model_info
                    for key, value in model_details.items():
                        print(f"{key.capitalize()}: {value}")

                print("-" * 40)

        else:
            (
                print("LM Studio has no model loaded.")
                if loaded_models
                else print("LM Studio is not active.")
            )
