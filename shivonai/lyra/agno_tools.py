"""
Agno integration for MCP Server tools.
"""
from typing import List, Dict, Any, Optional, Union, Callable
import functools
import json

from shivonai.core.mcp_client import MCPClient
from shivonai.utils.helpers import create_tool_description


def agno_toolkit(auth_token: str, base_url: str = "http://localhost:5000") -> List[Dict[str, Any]]:
    """Create Agno tools from MCP Server.
    
    Args:
        auth_token: Authentication token for MCP Server
        base_url: URL of the MCP server
        
    Returns:
        List of tool specifications for Agno
    """
    try:
        from agno.agent import Agent
    except ImportError:
        raise ImportError(
            "Could not import agno. "
            "Please install it with `pip install agno`."
        )
    
    # Set up client and authenticate
    client = MCPClient(base_url)
    client.authenticate(auth_token)
    
    # Get available tools
    available_tools = client.list_tools()
    
    # Format tools to match Agno/Claude JSON Schema draft 2020-12 format
    tool_specs = []
    
    for tool_info in available_tools:
        tool_name = tool_info["name"]
        tool_description = tool_info.get("description", "")
        
        # Create the JSON Schema compliant parameters object
        parameters = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        # Process the parameters from the MCP server
        for param in tool_info.get("parameters", []):
            param_name = param.get("name")
            param_description = param.get("description", "")
            param_type = param.get("type", "string")
            param_required = param.get("required", False)
            
            # Map MCP parameter types to JSON Schema types
            json_type = param_type
            if param_type not in ["string", "number", "integer", "boolean", "array", "object", "null"]:
                json_type = "string"  # Default to string for unknown types
            
            # Add parameter to properties
            parameters["properties"][param_name] = {
                "type": json_type,
                "description": param_description
            }
            
            # Add to required list if necessary
            if param_required:
                parameters["required"].append(param_name)
        
        # Create the tool spec in the format Claude expects
        tool_spec = {
            "type": "function",
            "function": {
                "name": tool_name,
                "description": tool_description,
                "parameters": parameters
            }
        }
        
        # Add the tool to our list
        tool_specs.append(tool_spec)
    
    # Create a wrapper class to handle the MCP client interaction
    class MCPToolset:
        def __init__(self, client, tools):
            self.client = client
            self.tools = tools
            self.specs = tool_specs
        
        def get_function_tool(self, name):
            """Get a function for the specified tool name."""
            def tool_function(**kwargs):
                """Tool function that calls the MCP server."""
                return self.client.call_tool(name, kwargs)
            return tool_function
        
        def __iter__(self):
            """Make the toolset iterable."""
            for tool in self.tools:
                tool_name = tool["function"]["name"]
                yield self.get_function_tool(tool_name)
    
    # Return an instance that can be used with Agno
    return MCPToolset(client, tool_specs)