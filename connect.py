import autogen
import agents_ls
from agent_ls import AgentType


def conversation():
    agent_manager = agents_ls.AgentManagerLS()
    # model_name="internlm2_5-20b-chat-q3_k_m.gguf"
    print("Init conversation")
    
    steve_assistant = agent_manager.create(AgentType.ASSISTANT_AGENT, name="Steve")
    user_proxy = agent_manager.create(AgentType.USER_PROXY_AGENT, name="User")
    
    user_proxy.initiate_chat(steve_assistant, message="Tell me an interesting fact!")

def test():
    agent_manager = agents_ls.AgentManagerLS()
    
    user_proxy = agent_manager.create(AgentType.USER_PROXY_AGENT, name="User_proxy")
    user_proxy.code_execution_config={"last_n_messages": 2, "work_dir": "coding", "use_docker": True}
    user_proxy.code_human_input_mode="TERMINATE"
    
    engineer = agent_manager.create(AgentType.ASSISTANT_AGENT, name="Engineer") 
    scientist = agent_manager.create(AgentType.ASSISTANT_AGENT, name="scientistAgentType")
    planner = agent_manager.create(AgentType.ASSISTANT_AGENT, name="plannerAgentType") 
    critic = agent_manager.create(AgentType.ASSISTANT_AGENT, name="criticAgentType")
    
    agents = [user_proxy, engineer, scientist, planner, critic]
    
    group_chat = agent_manager.create(AgentType.GROUP_CHAT, params={ "agents": agents})
    
    #print(group_chat[])
    
    #print("AGENTS in list:")
    #print(*agents)
    #map(print, agents)

    print("Fine")
    
    
def group_chat():
    
    
    agent_manager = agents_ls.AgentManagerLS()
    
    user_proxy = agent_manager.create(AgentType.USER_PROXY_AGENT, name="User_proxy")
    user_proxy.code_execution_config={"last_n_messages": 2, "work_dir": "coding", "use_docker": True}
    user_proxy.code_human_input_mode="TERMINATE"
    
    engineer = agent_manager.create(AgentType.ASSISTANT_AGENT, name="Engineer") 
    scientist = agent_manager.create(AgentType.ASSISTANT_AGENT, name="scientistAgentType")
    planner = agent_manager.create(AgentType.ASSISTANT_AGENT, name="plannerAgentType") 
    critic = agent_manager.create(AgentType.ASSISTANT_AGENT, name="criticAgentType")
    
    agents = [user_proxy, engineer, scientist, planner, critic]

    group_chat = agent_manager.create(AgentType.GROUP_CHAT, params={ "agents": agents})
    group_chat_manager = agent_manager.create(AgentType.GROUP_CHAT_MANAGER, params={"groupchat": group_chat})
    
    user_proxy.initiate_chat(
        group_chat_manager,
        message="""
        Who are the most famous artist in the world
        """,
    )
    
    
def display_menu():
    print("\n--- Main Menu ---")
    print("1. Start a conversation")
    print("2. Join a group chat")
    print("100. Test")
    print("3. Exit")
    print("----------------")

def get_user_choice():
    while True:
        choice = input("Enter your choice (1-3): ")
        if choice in ['1', '2', '100', '3']:
            return int(choice)
        else:
            print("Invalid input. Please enter a number between 1 and 3.")

if __name__ == "__main__":
    while True:
        display_menu()
        user_choice = get_user_choice()
        
        if user_choice == 1:
            conversation()
        elif user_choice == 2:
            group_chat()
        elif user_choice == 100:
            test()
        elif user_choice == 3:
            print("Exiting the program. Goodbye!")
            break
        
        input("\nPress Enter to return to the main menu...")