from agno.agent import Agent
from agno.models.openai import OpenAIChat
from shivonai.lyra import agno_toolkit
import os

# Replace with your actual MCP server details
auth_token = "KCeyMtsuklOtiJNM150wZrA4sCl9CtJd"
base_url = "http://localhost:5000"  # Your MCP server URL

os.environ["OPENAI_API_KEY"] = "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"

# Get Agno tools
tools = agno_toolkit(auth_token, base_url)
print(tools)
# Print available tools
print(f"Available tools: {[tool.name for tool in tools]}")

# Create an Agno agent with tools
agent = Agent(
    model=OpenAIChat(id="gpt-3.5-turbo"),
    tools=tools,
    markdown=True,
    show_tool_calls=True
)

# Try the agent with a simple task
try:
    agent.print_response("what listings I have?", stream=True)
except Exception as e:
    print(f"Error: {e}")