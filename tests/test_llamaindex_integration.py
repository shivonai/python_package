import unittest
from unittest.mock import patch, MagicMock

# Import the module to test
from shivonai.lyra.llamaindex_tools import llamaindex_toolkit


class TestLlamaIndexIntegration(unittest.TestCase):
    """Test cases for LlamaIndex integration."""
    
    @patch('shivonai.core.mcp_client.MCPClient')
    def test_llamaindex_toolkit(self, mock_client_class):
        """Test llamaindex_toolkit function."""
        # Configure mock
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        mock_client.authenticate.return_value = {"name": "Test Server", "version": "1.0"}
        mock_client.list_tools.return_value = [
            {
                "name": "weather",
                "description": "Get weather information",
                "parameters": [
                    {
                        "name": "location",
                        "type": "string",
                        "description": "City name",
                        "required": True
                    }
                ]
            }
        ]
        
        # Mock the FunctionTool import
        with patch('llama_index.core.tools.FunctionTool') as mock_function_tool:
            mock_function_tool.from_defaults.return_value = MagicMock()
            
            # Call the function
            tools = llamaindex_toolkit("test-token", "http://test-server:5000")
            
            # Assert
            mock_client_class.assert_called_once_with("http://test-server:5000")
            mock_client.authenticate.assert_called_once_with("test-token")
            mock_client.list_tools.assert_called_once()
            
            # Check that we got the expected tools
            self.assertEqual(len(tools), 1)
            self.assertIn("weather", tools)
            
            # Check that FunctionTool.from_defaults was called with correct parameters
            mock_function_tool.from_defaults.assert_called_once()
            call_args = mock_function_tool.from_defaults.call_args[1]
            self.assertEqual(call_args['name'], "weather")
            self.assertIn("Get weather information", call_args['description'])
    
    @patch('shivonai.core.mcp_client.MCPClient')
    def test_tool_function_calls_mcp_client(self, mock_client_class):
        """Test that the tool function calls the MCP client."""
        # Configure mock
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        mock_client.authenticate.return_value = {"name": "Test Server", "version": "1.0"}
        mock_client.list_tools.return_value = [
            {
                "name": "echo",
                "description": "Echo back the input",
                "parameters": [
                    {
                        "name": "message",
                        "type": "string",
                        "description": "Message to echo",
                        "required": True
                    }
                ]
            }
        ]
        mock_client.call_tool.return_value = "Hello, world!"
        
        # Create a fake FunctionTool that captures the function
        captured_fn = None
        
        class FakeFunctionTool:
            @staticmethod
            def from_defaults(name, description, fn):
                nonlocal captured_fn
                captured_fn = fn
                return MagicMock()
        
        # Mock the FunctionTool import
        with patch('llama_index.core.tools.FunctionTool', FakeFunctionTool):
            # Call the function to get the tools
            tools = llamaindex_toolkit("test-token", "http://test-server:5000")
            
            # Now call the captured function
            self.assertIsNotNone(captured_fn)
            result = captured_fn(message="Hello, world!")
            
            # Assert
            mock_client.call_tool.assert_called_once_with("echo", {"message": "Hello, world!"})
            self.assertEqual(result, "Hello, world!")


if __name__ == '__main__':
    unittest.main()