"""
CrewAI integration for MCP Server tools.
"""
from typing import List, Dict, Any, Optional

from shivonai.core.mcp_client import MCPClient
from shivonai.utils.helpers import parse_tool_parameters, create_tool_description


def crew_toolkit(auth_token: str, base_url: str = "http://localhost:5000") -> List[Any]:
    """Create CrewAI tools from MCP Server.
    
    Args:
        auth_token: Authentication token for MCP Server
        base_url: URL of the MCP server
        
    Returns:
        List of CrewAI tools
    """
    try:
        from crewai.tools import BaseTool
    except ImportError:
        raise ImportError(
            "Could not import crewai. "
            "Please install it with `pip install crewai`."
        )

    client = MCPClient(base_url)
    client.authenticate(auth_token)
    available_tools = client.list_tools()
    
    crew_tools = []
    
    for tool_info in available_tools:
        # Define a class that inherits from BaseTool for each MCP tool
        tool_name = tool_info["name"]
        tool_description = tool_info.get("description", "")
        tool_parameters = tool_info.get("parameters", [])
        
        # Create the full description including parameters
        full_description = create_tool_description(
            tool_name,
            tool_description,
            tool_parameters
        )
        
        # Create a class that inherits from BaseTool
        class MCPTool(BaseTool):
            name = tool_name
            description = full_description
            
            def _run(self, input_str):
                # Parse input string using the helper function
                args = parse_tool_parameters(input_str)
                return client.call_tool(tool_name, args)
        
        # Instantiate the tool
        crew_tools.append(MCPTool())
    
    return crew_tools