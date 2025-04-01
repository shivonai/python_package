"""
Test script for LlamaIndex integration with ShivonAI package.
This demonstrates how to use the llamaindex_toolkit to create and use tools.
"""
import os

from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent
from shivonai.lyra import llamaindex_toolkit

# Set up OpenAI API key - you'll need this to use OpenAI models with LlamaIndex
os.environ["OPENAI_API_KEY"] = "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"

# Your MCP server authentication details
MCP_AUTH_TOKEN = "KCeyMtsuklOtiJNM150wZrA4sCl9CtJd"
MCP_SERVER_URL = "http://localhost:5000"  # Change this to your server URL

def main():
    """Test LlamaIndex integration with ShivonAI."""
    print("Testing LlamaIndex integration with ShivonAI...")
    
    # Get LlamaIndex tools from your MCP server
    tools = llamaindex_toolkit(MCP_AUTH_TOKEN, MCP_SERVER_URL)
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