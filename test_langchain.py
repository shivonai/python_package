from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from shivonai.lyra import langchain_toolkit

# Replace with your actual MCP server details
auth_token = "KCeyMtsuklOtiJNM150wZrA4sCl9CtJd"
base_url = "http://localhost:5000"  # Your MCP server URL
# Get LangChain tools
tools = langchain_toolkit(auth_token, base_url)

# Print available tools
print(f"Available tools: {[tool.name for tool in tools]}")

# Initialize LangChain agent with tools
llm = ChatOpenAI(
            temperature=0,
            model_name="gpt-4-turbo",
            openai_api_key="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"
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