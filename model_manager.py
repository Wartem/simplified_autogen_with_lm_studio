import json
import os
import lm_studio_manager

base_url = "http://localhost:1234/v1"
api_key = "lm-studio"
lsm = lm_studio_manager.LMStudioManager()
config_file_name = "model_library.json"

def get_short_name(model):
    return model.rsplit('/', 1)[-1]

def create_model_config(model_name, max_tokens=1024, temperature=0.7):
    return {
        f"{get_short_name(model_name)}": {
            "config_list": [
                {
                    "model": model_name,
                    "base_url": base_url,
                    "api_key": api_key,
                    "temperature": temperature
                },
            ],
            "cache_seed": None,
            "max_tokens": max_tokens
        }
    }
    
# "status": "active", "models"
def load_and_save_models():
    models_and_status = lsm.get_status_and_loaded_models()
    
    if models_and_status["status"] == "error":
        print("LM Studio Error", models_and_status["message"])
        return []
    
    models = models_and_status["models"]
    
    if not models:
        print("LM Studio is not active")
        return []
    
    print("Models", models)
    
    # Convert the list of models to a dictionary
    model_dict = [create_model_config(model) for model in models]
    save_model_library(config_file_name, model_dict)
    
    return models 
    
    
def load_model_library(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_model_library(filename, model_configs: list):
    # Load the existing data from the file
    existing_data = load_model_library(filename)

    # Add only new models, without overwriting existing ones
    for config in model_configs:
        for key, value in config.items():
            if key not in existing_data:
                existing_data[key] = value

    # Write the updated data back to the file
    with open(filename, 'w') as f:
        json.dump(existing_data, f, indent=4)


def add_model_to_library(model_library, name, model_config):
    if name in model_library:
        print(f"Model {name} already exists. Skipping addition.")
    else:
        model_library[name] = model_config


def load_models_from_json(filename):
    loaded_models = load_model_library(filename)
    model_library = {}

    for model_name, model_data in loaded_models.items():
        config_list = model_data["config_list"]
        if config_list:
            model_config = config_list[0]
            model_library[model_name] = create_model_config(
                model_name=model_config["model"],
                max_tokens=model_data["max_tokens"],
                temperature=model_config["temperature"]
            )
    
    return model_library