import autogen
from enum import Enum
import uuid

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
    AgentType.CONVERSABLE_AGENT: lambda params: autogen.ConversableAgent(**params),
    AgentType.ASSISTANT_AGENT: lambda params: autogen.AssistantAgent(**params),
    AgentType.USER_PROXY_AGENT: lambda params: autogen.UserProxyAgent(**params),
    AgentType.RETRIEVE_USER_PROXY_AGENT: lambda params: autogen.RetrieveUserProxyAgent(**params),
    AgentType.TEACHABLE_AGENT: lambda params: autogen.TeachableAgent(**params),
    AgentType.AUTOGEN_CODER: lambda params: autogen.AutoGenCoder(**params),
    AgentType.CONFIGURABLE_AGENT: lambda params: autogen.ConfigurableAgent(**params),
    AgentType.HUMAN_PROXY_AGENT: lambda params: autogen.HumanProxyAgent(**params),
    AgentType.GROUP_CHAT: lambda params: autogen.GroupChat(**params),
    AgentType.GROUP_CHAT_MANAGER: lambda params: autogen.GroupChatManager(**params),
}

def create_agent(agent_type, name="", model_config=None, obj=None, **kwargs):
    if agent_type not in AGENT_CREATORS:
        raise ValueError(f"Unknown agent type: {agent_type}")

    agent_params = {
        "name": name or f"Agent_{uuid.uuid4().hex[:8]}",
        "llm_config": model_config,
        "code_execution_config": default_code_execution_config,
    }
    
    if agent_type in AGENTS_USING_NAMES:
        agent_params["system_message"] = f"You are an AI assistant named {agent_params['name']}."
    
    agent_params.update(kwargs)
    
    if agent_type == AgentType.GROUP_CHAT:
        return AGENT_CREATORS[agent_type](obj)
    elif agent_type == AgentType.GROUP_CHAT_MANAGER:
        return AGENT_CREATORS[agent_type](groupchat=obj)
    else:
        return AGENT_CREATORS[agent_type](agent_params)