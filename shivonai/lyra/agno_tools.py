"""
Agno integration for MCP Server tools.
"""
from typing import List, Dict, Any, Optional, Callable, Union
import functools
import inspect
import json

from shivonai.core.mcp_client import MCPClient
from shivonai.utils.helpers import create_tool_description


def agno_toolkit(auth_token: str, base_url: str = "http://localhost:5000") -> Dict[str, Callable]:
    """Create Agno tools from MCP Server.
    
    Args:
        auth_token: Authentication token for MCP Server
        base_url: URL of the MCP server
        
    Returns:
        Dictionary of Agno tool functions
    """
    try:
        # Import required Agno modules
        from agno.agent import Agent
    except ImportError:
        raise ImportError(
            "Could not import agno. "
            "Please install it with `pip install agno`."
        )

    client = MCPClient(base_url)
    client.authenticate(auth_token)
    available_tools = client.list_tools()
    
    # Dictionary to store our created tools
    agno_tools = {}
    
    # Create functions for each MCP tool
    for tool_info in available_tools:
        tool_name = tool_info["name"]
        tool_description = tool_info.get("description", "")
        tool_parameters = tool_info.get("parameters", [])
        
        # Create the function that will handle the tool call
        def make_tool_func(name, description, parameters):
            def tool_func(**kwargs):
                # Call the MCP tool and get the response
                response = client.call_tool(name, kwargs)
                
                # Convert the response to a string if it's a list or dictionary
                # This is important for compatibility with Agno and OpenAI's expectations
                if isinstance(response, (list, dict)):
                    return json.dumps(response, indent=2)
                return response
            
            # Create full description with parameters for the docstring
            full_description = create_tool_description(name, description, parameters)
            tool_func.__doc__ = full_description
            tool_func.__name__ = name
            
            return tool_func
        
        # Create the function for this specific tool
        func = make_tool_func(tool_name, tool_description, tool_parameters)
        
        # Store the function in our dictionary
        agno_tools[tool_name] = func
    
    return agno_tools


def create_agno_agent_with_mcp_tools(
    auth_token: str, 
    base_url: str = "http://localhost:5000",
    model: Any = None,
    instructions: Union[str, List[str]] = None,
    description: str = None,
    show_tool_calls: bool = True,
    markdown: bool = True
) -> Any:
    """Create an Agno agent with MCP tools.
    
    Args:
        auth_token: Authentication token for MCP Server
        base_url: URL of the MCP server
        model: The LLM model to use with the agent
        instructions: Instructions for the agent
        description: Description of the agent
        show_tool_calls: Whether to show tool calls in the agent's response
        markdown: Whether to render responses as markdown
        
    Returns:
        An Agno agent with MCP tools
    """
    try:
        from agno.agent import Agent
    except ImportError:
        raise ImportError("Could not import agno. Please install it with `pip install agno`.")
    
    # Get MCP tools as functions
    tools_dict = agno_toolkit(auth_token, base_url)
    tools = list(tools_dict.values())
    
    # Print available tools for debugging
    tool_names = [tool.__name__ for tool in tools]
    print(f"Available MCP tools for Agno: {tool_names}")
    
    # Create an Agno agent with the tools
    agent = Agent(
        model=model,
        instructions=instructions,
        description=description,
        tools=tools,
        show_tool_calls=show_tool_calls,
        markdown=markdown
    )
    
    return agent


# Function to get the available tools
def get_available_mcp_tools(auth_token: str, base_url: str = "http://localhost:5000") -> List[str]:
    """Get a list of available MCP tool names.
    
    Args:
        auth_token: Authentication token for MCP Server
        base_url: URL of the MCP server
        
    Returns:
        List of tool names
    """
    tools_dict = agno_toolkit(auth_token, base_url)
    return list(tools_dict.keys())
