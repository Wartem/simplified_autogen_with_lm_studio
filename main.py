from config_manager import ConfigManager
from lm_studio_manager import LMStudioManager
from agent_factory import AgentType, create_agent

class AgentManager:
    def __init__(self, config_file):
        self.config_manager = ConfigManager(config_file)
        self.lm_studio = LMStudioManager()

    def create_agent(self, agent_type, name="", model_name="", obj=None, **kwargs):
        if agent_type in [AgentType.GROUP_CHAT, AgentType.GROUP_CHAT_MANAGER]:
            return create_agent(agent_type, name=name, obj=obj, **kwargs)

        if not model_name:
            model_config = self.config_manager.get_random_model_config()
        else:
            model_config = self.config_manager.get_model_config(model_name)

        if not model_config:
            raise ValueError("No valid model configuration found.")

        return create_agent(agent_type, name, model_config, **kwargs)

    def start_conversation(self):
        user_proxy = self.create_agent(AgentType.USER_PROXY_AGENT, name="User")
        assistant = self.create_agent(AgentType.ASSISTANT_AGENT, name="Assistant")
        user_proxy.initiate_chat(assistant, message="Tell me an interesting fact!")

    def start_group_chat(self):
        user_proxy = self.create_agent(AgentType.USER_PROXY_AGENT, name="User_proxy")
        engineer = self.create_agent(AgentType.ASSISTANT_AGENT, name="Engineer")
        scientist = self.create_agent(AgentType.ASSISTANT_AGENT, name="Scientist")
        planner = self.create_agent(AgentType.ASSISTANT_AGENT, name="Planner")
        critic = self.create_agent(AgentType.ASSISTANT_AGENT, name="Critic")

        group_chat = self.create_agent(AgentType.GROUP_CHAT, obj=[user_proxy, engineer, scientist, planner, critic])
        group_chat_manager = self.create_agent(AgentType.GROUP_CHAT_MANAGER, obj=group_chat)

        user_proxy.initiate_chat(group_chat_manager, message="Let's discuss the future of AI.")

def main():
    agent_manager = AgentManager("model_library.json")

    while True:
        print("\n--- Main Menu ---")
        print("1. Start a conversation")
        print("2. Join a group chat")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            agent_manager.start_conversation()
        elif choice == '2':
            agent_manager.start_group_chat()
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid input. Please enter a number between 1 and 3.")

        input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    main()