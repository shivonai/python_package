import unittest
from unittest.mock import patch, MagicMock

# Import the module to test
from shivonai.lyra.agno_tools import agno_toolkit


class TestAgnoIntegration(unittest.TestCase):
    """Test cases for Agno integration."""
    
    @patch('shivonai.core.mcp_client.MCPClient')
    def test_agno_toolkit(self, mock_client_class):
        """Test agno_toolkit function."""
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
        
        # Mock the Agno Agent import
        with patch('agno.agent.Agent', create=True):
            # Call the function
            tools = agno_toolkit("test-token", "http://test-server:5000")
            
            # Assert
            mock_client_class.assert_called_once_with("http://test-server:5000")
            mock_client.authenticate.assert_called_once_with("test-token")
            mock_client.list_tools.assert_called_once()
            
            # Check that we got the expected tools
            self.assertEqual(len(tools), 1)
            
            # Check that the tool is a function with the correct attributes
            tool = tools[0]
            self.assertTrue(callable(tool))
            self.assertEqual(tool.__name__, "weather")
            self.assertIn("Get weather information", tool.__doc__)
    
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
        
        # Mock the Agno Agent import
        with patch('agno.agent.Agent', create=True):
            # Call the function to get the tools
            tools = agno_toolkit("test-token", "http://test-server:5000")
            
            # Call the tool function
            result = tools[0](message="Hello, world!")
            
            # Assert
            mock_client.call_tool.assert_called_once_with("echo", {"message": "Hello, world!"})
            self.assertEqual(result, "Hello, world!")


if __name__ == '__main__':
    unittest.main()