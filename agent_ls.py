from enum import Enum
import autogen

class AgentType(Enum):
    CONVERSABLE_AGENT = "conversable_agent"
    ASSISTANT_AGENT = "assistant_agent"
    USER_PROXY_AGENT = "user_proxy_agent"
    RETRIEVE_USER_PROXY_AGENT = "retrieve_user_proxy_agent"
    GROUP_CHAT_MANAGER = "group_chat_manager"
    TEACHABLE_AGENT = "teachable_agent"
    AUTOGEN_CODER = "autogen_coder"
    CONFIGURABLE_AGENT = "configurable_agent"
    HUMAN_PROXY_AGENT = "human_proxy_agent"
    GROUP_CHAT = "chat_group"
    
AGENTS_USING_NAMES = [
    AgentType.CONVERSABLE_AGENT,
    AgentType.ASSISTANT_AGENT,
    AgentType.USER_PROXY_AGENT,
    AgentType.TEACHABLE_AGENT,
    AgentType.AUTOGEN_CODER,
    AgentType.CONFIGURABLE_AGENT,
    AgentType.HUMAN_PROXY_AGENT,
]

default_code_execution_config = {"use_docker": True}
    
AGENT_CREATORS = {
    AgentType.CONVERSABLE_AGENT: lambda params: autogen.ConversableAgent(
        system_message="You are a conversable AI assistant.", 
        code_execution_config=default_code_execution_config,
        name = params["name"],
        llm_config = params["llm_config"]
    ),
    AgentType.ASSISTANT_AGENT: lambda params: autogen.AssistantAgent(
        system_message="You are an AI assistant that helps with tasks.", 
        code_execution_config=default_code_execution_config,
        name = params["name"],
        llm_config = params["llm_config"]
    ),
    AgentType.USER_PROXY_AGENT: lambda params: autogen.UserProxyAgent(
        system_message="You are a proxy for the human user. You are the human admin",
        human_input_mode="ALWAYS",
        max_consecutive_auto_reply=10, 
        code_execution_config=default_code_execution_config,
        name = params["name"],
        llm_config = params["llm_config"]
    ),
    AgentType.RETRIEVE_USER_PROXY_AGENT: lambda params: autogen.RetrieveUserProxyAgent(
        system_message="You are a proxy for the human user with retrieval capabilities.",
        human_input_mode="ALWAYS",
        max_consecutive_auto_reply=10,
        retrieve_config={"task": "qa", "docs_path": "path/to/your/documents"},
        code_execution_config=default_code_execution_config,
        name = params["name"],
        llm_config = params["llm_config"]
    ),
    AgentType.TEACHABLE_AGENT: lambda params: autogen.TeachableAgent(
        system_message="You are an AI assistant that can learn from interactions.",
        teach_config={"verbosity": 0, "reset_db": False, "path_to_db_dir": "./teachable_agent_db"},
        code_execution_config=default_code_execution_config,
        name = params["name"],
        llm_config = params["llm_config"]
    ),
    AgentType.AUTOGEN_CODER: lambda params: autogen.AutoGenCoder(
        system_message="You are an AI assistant specialized in coding tasks.", 
        code_execution_config=default_code_execution_config,
        llm_config = params["llm_config"]
    ),
    AgentType.CONFIGURABLE_AGENT: lambda params: autogen.ConfigurableAgent(
        system_message="You are a configurable AI assistant.",
        human_input_mode="NEVER", 
        code_execution_config=default_code_execution_config,
        name = params["name"],
        llm_config = params["llm_config"]
    ),
    AgentType.HUMAN_PROXY_AGENT: lambda params: autogen.HumanProxyAgent(
        system_message="You are a human proxy agent.",
        human_input_mode="ALWAYS",
        code_execution_config=default_code_execution_config,
        name = params["name"],
        llm_config = params["llm_config"]
    ),
    AgentType.GROUP_CHAT: lambda params: autogen.GroupChat(
        agents=params["params"]["agents"],
        messages=params.get("messages", []),
        max_round=params.get("max_round", 12),
        # speaker_selection_method=params.get("speaker_selection_method", "round_robin"),
        # allow_repeat_speaker=params.get("allow_repeat_speaker", False), 
        # llm_config=params.get("llm_config", None)
    ),
    AgentType.GROUP_CHAT_MANAGER: lambda params: autogen.GroupChatManager(
        # messages=params.get("messages", None),
        # max_round=params.get("max_round", 12),
        # speaker_selection_method=params.get("speaker_selection_method", "round_robin"),
        # allow_repeat_speaker=params.get("allow_repeat_speaker", False), 
        
        system_message = "You are managing a group chat.",
        groupchat=params["params"]["groupchat"]
        
        # human_input_mode = "NEVER",
        # llm_config=params.get("llm_config", None)
    ),
}
