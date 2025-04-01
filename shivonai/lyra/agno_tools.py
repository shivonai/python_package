# """
# Agno integration for MCP Server tools.
# """
# from typing import List, Dict, Any, Optional, Union, Callable

# from shivonai.core.mcp_client import MCPClient
# from shivonai.utils.helpers import parse_arguments


# def agno_toolkit(auth_token: str, base_url: str = "http://localhost:5000"):
#     """Create Agno tools from MCP Server.
    
#     Args:
#         auth_token: Authentication token for MCP Server
#         base_url: URL of the MCP server
        
#     Returns:
#         List of Agno tools
#     """
#     try:
#         import agno
#     except ImportError:
#         raise ImportError(
#             "Could not import agno. "
#             "Please install it with `pip install agno`."
#         )

#     client = MCPClient(base_url)
#     client.authenticate(auth_token)
#     available_tools = client.list_tools()
    
#     # In Agno, tools are typically defined as custom classes with methods
#     class MCPTools:
#         """MCP tools for Agno."""
        
#         def __init__(self, client, tool_infos):
#             """Initialize MCP tools.
            
#             Args:
#                 client: MCP client
#                 tool_infos: List of tool information dictionaries
#             """
#             self.client = client
#             self.tool_infos = tool_infos
            
#             # Dynamically create methods for each tool
#             for tool_info in tool_infos:
#                 self._create_tool_method(tool_info)
        
#         def _create_tool_method(self, tool_info):
#             """Create a method for a tool.
            
#             Args:
#                 tool_info: Tool information dictionary
#             """
#             tool_name = tool_info["name"]
            
#             # Define the function that will call the MCP tool
#             def tool_method(self, query_str):
#                 """Call the MCP tool."""
#                 args = parse_arguments(query_str)
#                 return self.client.call_tool(tool_name, args)
            
#             # Set docstring for the method
#             param_desc = "Parameters:\n"
#             for param in tool_info.get("parameters", []):
#                 required = "Required" if param.get("required", False) else "Optional"
#                 param_desc += f"- {param['name']} ({param.get('type', 'any')}): {param.get('description', '')} [{required}]\n"
            
#             tool_method.__doc__ = f"{tool_info.get('description', '')}\n\n{param_desc}"
            
#             # Set the function as a method of the instance
#             setattr(self, tool_name, tool_method.__get__(self))
    
#     # Create a single MCPTools instance for all tools
#     mcp_tools = MCPTools(client, available_tools)
    
#     return mcp_tools


# def create_agno_agent(
#     model,
#     auth_token: str,
#     base_url: str = "http://localhost:5000",
#     **agent_kwargs
# ):
#     """Create an Agno agent with MCP tools.
    
#     Args:
#         model: Agno model
#         auth_token: Authentication token for MCP Server
#         base_url: URL of the MCP server
#         **agent_kwargs: Additional arguments for the Agno agent
        
#     Returns:
#         Agno agent
#     """
#     try:
#         from agno.agent import Agent
#     except ImportError:
#         raise ImportError(
#             "Could not import agno. "
#             "Please install it with `pip install agno`."
#         )
    
#     tools = agno_toolkit(auth_token, base_url)
    
#     agent = Agent(
#         model=model,
#         tools=[tools],  # Agno expects a list of tool objects
#         **agent_kwargs
#     )
    
#     return agent

"""
Agno integration for MCP Server tools.
"""
from typing import List, Dict, Any, Optional, Union, Callable

from shivonai.core.mcp_client import MCPClient
from shivonai.utils.helpers import create_tool_description


def agno_toolkit(auth_token: str, base_url: str = "http://localhost:5000") -> List[Any]:
    """Create Agno tools from MCP Server.
    
    Args:
        auth_token: Authentication token for MCP Server
        base_url: URL of the MCP server
        
    Returns:
        List of Agno tools
    """
    try:
        # Try importing from agno.tools first 
        from agno.tools import Tool
    except ImportError:
        try:
            # Fallback to importing the Agent class which we'll use to create a custom tool
            from agno.agent import Agent
        except ImportError:
            raise ImportError(
                "Could not import agno. "
                "Please install it with `pip install agno`."
            )

    client = MCPClient(base_url)
    client.authenticate(auth_token)
    available_tools = client.list_tools()
    
    # Create a custom class for MCP tools
    class MCPTool:
        """Custom class for MCP tools to be used with Agno."""
        
        def __init__(self, name, description, client, parameters=None):
            """Initialize an MCP tool.
            
            Args:
                name: Name of the tool
                description: Description of the tool
                client: MCP client
                parameters: List of parameters for the tool
            """
            self.name = name
            self.description = create_tool_description(name, description, parameters or [])
            self.client = client
            
        def __call__(self, **kwargs):
            """Call the tool with the given parameters."""
            return self.client.call_tool(self.name, kwargs)
    
    # Create tools for each available MCP tool
    agno_tools = []
    
    for tool_info in available_tools:
        # Create an MCP tool for Agno
        tool = MCPTool(
            name=tool_info["name"],
            description=tool_info.get("description", ""),
            client=client,
            parameters=tool_info.get("parameters", [])
        )
        
        agno_tools.append(tool)
    
    return agno_tools