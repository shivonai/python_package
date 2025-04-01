# ShivonAI

A Python package for integrating MCP (Model Context Protocol) server tools with various AI agent frameworks.

## Features

- Connect to your MCP server and access custom tools
- Integrate MCP tools with popular AI agent frameworks:
  - LangChain
  - LlamaIndex
  - CrewAI
  - Agno

## Installation

You can install ShivonAI from PyPI:

```bash
pip install shivonai
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/yourusername/shivonai.git
```

## Getting Started

### Basic Usage

```python
from shivonai.core.mcp_client import MCPClient

# Initialize the client
client = MCPClient(base_url="http://your-mcp-server:5000")

# Authenticate with your token
server_info = client.authenticate("your-auth-token")

# List available tools
tools = client.list_tools()

# Call a tool
result = client.call_tool("tool_name", {"param1": "value1", "param2": "value2"})

print(result)
```

### LangChain Integration

```python
from langchain.llms import OpenAI
from shivonai.lyra import langchain_toolkit

# Get LangChain tools
tools = langchain_toolkit("your-auth-token", "http://your-mcp-server:5000")

# Use tools with your LangChain agent
from langchain.agents import initialize_agent, AgentType

llm = OpenAI(temperature=0)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Or use the convenience function
from shivonai.lyra.langchain_tools import create_langchain_agent

agent = create_langchain_agent(
    llm=llm,
    auth_token="your-auth-token",
    base_url="http://your-mcp-server:5000",
    verbose=True
)

# Run the agent
agent.run("Use my custom tool to accomplish this task")
```

### LlamaIndex Integration

```python
from llama_index.llms import OpenAI
from shivonai.lyra import llamaindex_toolkit

# Get LlamaIndex tools
tools = llamaindex_toolkit("your-auth-token", "http://your-mcp-server:5000")

# Use tools with your LlamaIndex agent
from llama_index.agent import ReActAgent

llm = OpenAI(temperature=0)
agent = ReActAgent.from_tools(
    tools=list(tools.values()),
    llm=llm,
    verbose=True
)

# Or use the convenience function
from shivonai.lyra.llamaindex_tools import create_llamaindex_agent

agent = create_llamaindex_agent(
    llm=llm,
    auth_token="your-auth-token",
    base_url="http://your-mcp-server:5000",
    verbose=True
)

# Run the agent
response = agent.chat("Use my custom tool to accomplish this task")
```

### CrewAI Integration

```python
from crewai import Agent, Crew, Task
from langchain.llms import OpenAI
from shivonai.lyra import crew_toolkit

# Get CrewAI tools
tools = crew_toolkit("your-auth-token", "http://your-mcp-server:5000")

# Create an agent with these tools
agent = Agent(
    role="Data Analyst",
    goal="Analyze data using custom tools",
    backstory="You are an expert data analyst with access to custom tools",
    verbose=True,
    llm=OpenAI(temperature=0),
    tools=tools
)

# Or use the convenience function
from shivonai.lyra.crew_tools import create_crew_agent

agent = create_crew_agent(
    llm=OpenAI(temperature=0),
    auth_token="your-auth-token",
    base_url="http://your-mcp-server:5000",
    role="Data Analyst",
    goal="Analyze data using custom tools",
    backstory="You are an expert data analyst with access to custom tools",
    verbose=True
)

# Use the agent in a crew
task = Task(
    description="Analyze the data and provide insights",
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

result = crew.kickoff()
```

### Agno Integration

```python
from agno.models.openai import OpenAIChat
from shivonai.lyra import agno_toolkit

# Get Agno tools
tools = agno_toolkit("your-auth-token", "http://your-mcp-server:5000")

# Create an agent with these tools
from agno.agent import Agent

agent = Agent(
    model=OpenAIChat(id="gpt-4"),
    tools=tools,
    markdown=True
)

# Or use the convenience function
from shivonai.lyra.agno_tools import create_agno_agent

agent = create_agno_agent(
    model=OpenAIChat(id="gpt-4"),
    auth_token="your-auth-token",
    base_url="http://your-mcp-server:5000",
    markdown=True
)

# Use the agent
agent.print_response("Use my custom tool to accomplish this task", stream=True)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.