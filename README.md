# ShivonAI

A Python package for integrating AI recruitment tools with various AI agent frameworks.

## Features

- Acess custom hiring tools for AI agents
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
pip install git+https://github.com/shivonai/python_package.git
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
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from shivonai.lyra import langchain_toolkit

# Replace with your actual MCP server details
auth_token = "shivonai_auth_token"

# Get LangChain tools
tools = langchain_toolkit(auth_token)

# Print available tools
print(f"Available tools: {[tool.name for tool in tools]}")

# Initialize LangChain agent with tools
llm = ChatOpenAI(
            temperature=0,
            model_name="gpt-4-turbo",
            openai_api_key="openai-api-key"
        )

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Try running the agent with a simple task
try:
    result = agent.run("what listing I have?")
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
```

### LlamaIndex Integration

```python
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent
from shivonai.lyra import llamaindex_toolkit

# Set up OpenAI API key - you'll need this to use OpenAI models with LlamaIndex
os.environ["OPENAI_API_KEY"] = "openai_api_key"

# Your MCP server authentication details
MCP_AUTH_TOKEN = "shivonai_auth_token"


def main():
    """Test LlamaIndex integration with ShivonAI."""
    print("Testing LlamaIndex integration with ShivonAI...")
    
    # Get LlamaIndex tools from your MCP server
    tools = llamaindex_toolkit(MCP_AUTH_TOKEN)
    print(f"Found {len(tools)} MCP tools for LlamaIndex:")
    
    for name, tool in tools.items():
        print(f"  - {name}: {tool.metadata.description[:60]}...")
    
    # Create a LlamaIndex agent with these tools
    llm = OpenAI(model="gpt-4")
    
    # Convert tools dictionary to a list
    tool_list = list(tools.values())
    
    # Create the ReAct agent
    agent = ReActAgent.from_tools(
        tools=tool_list,
        llm=llm,
        verbose=True
    )
    
    # Test the agent with a simple query that should use one of your tools
    # Replace this with a query that's relevant to your tools
    query = "what listings I have?"
    
    print("\nTesting agent with query:", query)
    response = agent.chat(query)
    
    print("\nAgent response:")
    print(response)

if __name__ == "__main__":
    main()
```

### CrewAI Integration

```python
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI  # or any other LLM you prefer
from shivonai.lyra import crew_toolkit
import os

os.environ["OPENAI_API_KEY"] = "oepnai_api_key"

llm = ChatOpenAI(temperature=0.7, model="gpt-4")

# Get CrewAI tools
tools = crew_toolkit("shivonai_auth_token")

# Print available tools
print(f"Available tools: {[tool.name for tool in tools]}")

# Create an agent with these tools
agent = Agent(
    role="Data Analyst",
    goal="Analyze data using custom tools",
    backstory="You're an expert data analyst with access to custom tools",
    tools=tools,
    llm=llm  # Provide the LLM here
)

# Create a task - note the expected_output field
task = Task(
    description="what listings I have?",
    expected_output="A detailed report with key insights and recommendations",
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task])

result = crew.kickoff()
print(result)
```

### Agno Integration

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from shivonai.lyra import agno_toolkit
import os
from agno.models.aws import Claude

# Replace with your actual MCP server details
auth_token = "Shivonai_auth_token"

os.environ["OPENAI_API_KEY"] = "oepnai_api_key"

# Get Agno tools
tools = agno_toolkit(auth_token)

# Print available tools
print(f"Available MCP tools: {list(tools.keys())}")

# Create an Agno agent with tools
agent = Agent(
    model=OpenAIChat(id="gpt-3.5-turbo"),
    tools=list(tools.values()),
    markdown=True,
    show_tool_calls=True
)

# Try the agent with a simple task
try:
    agent.print_response("what listing are there?", stream=True)
except Exception as e:
    print(f"Error: {e}")
```

## License

This project is licensed under a Proprietary License – see the LICENSE file for details.
