import json
import random
import uuid

import agent_ls
import model_manager
from agent_ls import AgentType, AGENT_CREATORS, AGENTS_USING_NAMES

config_file_name = "model_library.json"


class AgentManagerLS:
    '''
    Use AgentType Enum to see the agent types available.
    If a model is not specified, a random (loaded) model will be choosen.
    '''
    def __init__(self):
        self.model_configs = self.load_model_configs(config_file_name)
        self.loaded_models = model_manager.load_and_save_models()
        self.matched_models = self.match_models_with_configs(self.loaded_models, self.model_configs)
        
        # Default code execution config
        self.default_code_execution_config = {"use_docker": False}
        
        
    @staticmethod
    def load_model_configs(filename):
        with open(filename, 'r') as f:
            return json.load(f)


    @staticmethod
    def match_models_with_configs(loaded_models, model_configs):
        matched_models = {}
        for model in loaded_models:
            short_name = model.rsplit('/', 1)[-1]
            if short_name in model_configs:
                matched_models[short_name] = model_configs[short_name]
        return matched_models


    def get_available_models(self) -> str:
        return list(self.matched_models.keys())
    
    
    def print_available_models(self):
        print("\nAvailable models:")
        for model_name in self.get_available_models():
            print(f"- {model_name}")


    def create(self, agent_type: AgentType, name = "", model_name = "", **params):
        
        #print("agent_type", agent_type, "AGENT_CREATORS", AGENT_CREATORS)
        # group_chat = agent_manager.create("Chat Group", AgentType.CHAT_GROUP)
        if agent_type not in AGENT_CREATORS:
            
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        if not model_name:
            available_models = self.get_available_models()
            
            if available_models:
                model_name = random.choice(available_models)
                print(f"Agent {name} {agent_type} was assigned a random model: {model_name}")
        
        else:
            print(f"Agent {name} {agent_type} was assigned the model: {model_name}")
                
        if model_name and model_name not in self.matched_models:
            self.print_available_models()
            raise ValueError(f"Model {model_name} not found in available models.")

        model_config = self.matched_models[model_name]
        config_list = model_config['config_list']
        llm_config = {
            "config_list": config_list,
            "cache_seed": model_config['cache_seed'],
            "temperature": config_list[0]['temperature'],
            "max_tokens": model_config['max_tokens']
        }
        
        if agent_type in AGENTS_USING_NAMES:
            if not name:
                name = f"{model_name}_{uuid.uuid4().hex[:8]}"
            params.update({"name": name})
            
        params.update({"llm_config": llm_config})
        
        
        
        #if agent_type == AgentType.GROUP_CHAT:
            #if "agent_params" not in kwargs or "agents" not in kwargs["agent_params"] or not kwargs["agent_params"]["agents"]:
                #raise ValueError("GroupChat requires a non-empty list of agents in the 'agents' parameter.")
            #if "agents" not in kwargs or kwargs["agents"] is None:
                #raise ValueError("GroupChat requires a non-empty list of agents in the 'agents' parameter.")


        #print(params)
        
        print("---------------------------------------------", params)

        return AGENT_CREATORS[agent_type](params)


# Usage example
if __name__ == "__main__":
    agent_ls = AgentManagerLS()
    
    print("Available agent types:")
    for agent_type in AgentType:
        print(f"- {agent_type.name}")
    
    available_models = agent_ls.get_available_models()
    model = random.choice(available_models)
    
    if available_models:
        model = agent_ls.user_specified_model
        if not model:
            model = random.choice(available_models)
            
        conversable_agent = agent_ls.create(AgentType.CONVERSABLE_AGENT)
        
        # Create an assistant agent with the second available model (if there is one)
        if len(available_models) > 1:
            assistant_agent = agent_ls.create(AgentType.ASSISTANT_AGENT, available_models[1])
            print(f"Created an Assistant Agent: {assistant_agent.name}")
    else:
        print("No models available. Please check your model configurations.")
