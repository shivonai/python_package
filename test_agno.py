from agno.agent import Agent
from agno.models.openai import OpenAIChat
from shivonai.lyra import agno_toolkit
import os
from agno.models.aws import Claude

# Replace with your actual MCP server details
auth_token = "KCeyMtsuklOtiJNM150wZrA4sCl9CtJd"
base_url = "http://localhost:5000"  # Your MCP server URL

os.environ["OPENAI_API_KEY"] = "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"
os.environ["AWS_ACCESS_KEY_ID"] = "AKIAQFC27P4YVMU55MV7"
os.environ["AWS_SECRET_ACCESS_KEY"] = "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"
os.environ["AWS_REGION "] = "us-west-2"



# Get Agno tools
tools = agno_toolkit(auth_token, base_url)
print(tools)
# Print available tools
# print(tools.__name__)

print(f"Available tools: {[tool.__name__ for tool in tools]}")

# Create an Agno agent with tools
agent = Agent(
    # model=OpenAIChat(id="gpt-3.5-turbo"),
    model = Claude(id="anthropic.claude-3-5-sonnet-20240620-v1:0"),
    tools=tools,
    markdown=True,
    show_tool_calls=True
)

# Try the agent with a simple task
try:
    agent.print_response("use appropriate tool and let me know what listings I have? also for tool calling send valid json.", stream=True)
except Exception as e:
    print(f"Error: {e}")