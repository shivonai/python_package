"""
LangChain integration for MCP Server tools.
"""
from typing import List, Dict, Any, Optional

from langchain.tools import Tool

from shivonai.core.mcp_client import MCPClient
from shivonai.utils.helpers import parse_tool_parameters, create_tool_description


def langchain_toolkit(auth_token: str, base_url: str = "https://mcp-server.shivonai.com") -> List[Tool]:
    """Create LangChain tools from MCP Server.
    
    Args:
        auth_token: Authentication token for MCP Server
        base_url: URL of the MCP server
        
    Returns:
        List of LangChain tools
    """
    client = MCPClient(base_url)
    client.authenticate(auth_token)
    available_tools = client.list_tools()
    
    langchain_tools = []
    
    for tool_info in available_tools:
        # Create a function that will handle the tool
        def make_tool_func(name):
            def tool_func(arg_string):
                args = parse_tool_parameters(arg_string)
                return client.call_tool(name, args)
            return tool_func
        
        # Create the tool with the function
        tool_func = make_tool_func(tool_info["name"])
        
        # Create the full description including parameters
        full_description = create_tool_description(
            tool_info["name"],
            tool_info.get("description", ""),
            tool_info.get("parameters", [])
        )
        
        # Create the LangChain Tool
        langchain_tool = Tool(
            name=tool_info["name"],
            description=full_description,
            func=tool_func
        )
        
        langchain_tools.append(langchain_tool)
    
    return langchain_tools