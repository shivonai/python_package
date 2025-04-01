import unittest
from unittest.mock import patch, MagicMock

# Import the module to test
from shivonai.lyra.langchain_tools import langchain_toolkit


class TestLangChainIntegration(unittest.TestCase):
    """Test cases for LangChain integration."""
    
    @patch('shivonai.core.mcp_client.MCPClient')
    def test_langchain_toolkit(self, mock_client_class):
        """Test langchain_toolkit function."""
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
        
        # Call the function
        tools = langchain_toolkit("test-token", "http://test-server:5000")
        
        # Assert
        mock_client_class.assert_called_once_with("http://test-server:5000")
        mock_client.authenticate.assert_called_once_with("test-token")
        mock_client.list_tools.assert_called_once()
        
        # Check that we got the expected tools
        self.assertEqual(len(tools), 1)
        self.assertEqual(tools[0].name, "weather")
        self.assertIn("Get weather information", tools[0].description)
        self.assertIn("location (string): City name [Required]", tools[0].description)
    
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
        
        # Call the function to get the tools
        tools = langchain_toolkit("test-token", "http://test-server:5000")
        
        # Call the tool function
        result = tools[0].run('{"message": "Hello, world!"}')
        
        # Assert
        mock_client.call_tool.assert_called_once_with("echo", {"message": "Hello, world!"})
        self.assertEqual(result, "Hello, world!")


if __name__ == '__main__':
    unittest.main()