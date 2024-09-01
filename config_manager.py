import json
import random

class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.model_configs = self.load_model_configs()

    def load_model_configs(self):
        with open(self.config_file, 'r') as f:
            return json.load(f)

    def get_available_models(self):
        return list(self.model_configs.keys())

    def get_model_config(self, model_name):
        return self.model_configs.get(model_name)

    def get_random_model_config(self):
        available_models = self.get_available_models()
        if available_models:
            model_name = random.choice(available_models)
            return self.get_model_config(model_name)
        return None

    def update_model_config(self, model_name, config):
        self.model_configs[model_name] = config
        self.save_model_configs()

    def save_model_configs(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.model_configs, f, indent=4)