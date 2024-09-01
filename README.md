![Python](https://img.shields.io/badge/language-Python-blue.svg)
![AutoGen](https://img.shields.io/badge/framework-AutoGen-orange.svg)
![LM-Studio](https://img.shields.io/badge/LLM-LM--Studio-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Version](https://img.shields.io/badge/version-0.1.0-brightgreen.svg)
![AI](https://img.shields.io/badge/AI-enabled-blue.svg)
![Local LLM](https://img.shields.io/badge/LLM-Local-red.svg)

# Simplified Autogen with LM Studio
### Simplify agent creation in LM Studio with automated workflows, streamlining your experience and reducing complexity.

**Note:** This project is currently under development and is not intended to be viewed as a complete or production-ready solution. Features and functionality are still being added, and there may be bugs or incomplete sections.

## Overview
This project combines the power of Autogen, a framework for developing AI agents, with LM Studio, a tool for running large language models locally. It provides a simplified interface for creating and managing AI agents. Two simple examples are included, one-on-one conversations and group chats using locally hosted language models.

## Features

Easy Agent Creation: Quickly create various types of AI agents using the AgentManagerLS class.
Local Model Integration: Seamlessly use language models hosted on LM Studio.
Flexible Conversations: Support for both one-on-one conversations and group chats.
Model Management: Efficient handling of model configurations and loading.

## Prerequisites

- Python 3.8+
- Autogen library
- LM Studio (with models loaded)
- Docker

## Installation

Clone the repository:
```
git clone https://github.com/yourusername/simplified-autogen-lm-studio.git
cd simplified-autogen-lm-studio
```

### Optional: Create a virtual environment
```
python -m venv venv
```
### Activate the virtual environment

On Windows:
```
venv\Scripts\activate
```

On macOS and Linux:
```
source venv/bin/activate
```

### Install required packages:
```
pip install -r requirements.txt
```
Ensure LM Studio and Docker are installed and running with your desired models loaded.

## Configuration
Update the model_library.json file with your LM Studio model configurations.
Modify the base_url and api_key in model_manager.py if your LM Studio setup differs from the default.

## Usage
Run the main script to start interacting with the agents:
```
python main.py
```
This will present a menu with options to:

- Start a one-on-one conversation
- Join a group chat
- Exit the program

### Creating Agents
Use the AgentManagerLS class to create various types of agents:
```
agent_manager = agents_ls.AgentManagerLS()
assistant = agent_manager.create(AgentType.ASSISTANT_AGENT, name="Assistant")
user_proxy = agent_manager.create(AgentType.USER_PROXY_AGENT, name="User")
```

### Starting a Conversation
Initiate a chat between agents:
user_proxy.initiate_chat(assistant, message="Tell me an interesting fact!")

### Group Chat
Create multiple agents and a group chat:
```
agents = [user_proxy, engineer, scientist, planner, critic]
group_chat = agent_manager.create(AgentType.GROUP_CHAT, params={"agents": agents})
group_chat_manager = agent_manager.create(AgentType.GROUP_CHAT_MANAGER, params={"groupchat": group_chat})

user_proxy.initiate_chat(group_chat_manager, message="Let's discuss the future of AI.")
```

## Project Structure
- main.py: Entry point of the application.
 agents_ls.py: Defines the AgentManagerLS class and agent types.
- agent_ls.py: Contains agent type definitions and creation logic.
- lm_studio_manager.py: Manages interactions with LM Studio.
- model_manager.py: Handles model configurations and loading.
- model_library.json: Stores model configurations.

## Customization
Add new agent types in agent_ls.py.
Modify existing agent behaviors by updating their creation parameters in agents_ls.py.
Extend LMStudioManager in lm_studio_manager.py for additional LM Studio interactions.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer
This project is an independent initiative and is not connected to or endorsed by the teams behind AutoGen or LM Studio. While it utilizes the capabilities of these frameworks, it operates separately and is developed independently. Users should refer to the official documentation and resources provided by Microsoft for AutoGen and LM Studio for any support or inquiries related to those projects. This statement clearly communicates the independence of your project while acknowledging the technologies it leverages.

------------------
This project is for educational and research purposes. Ensure you comply with the terms of service of any language models you use.
