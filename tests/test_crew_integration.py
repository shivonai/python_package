import unittest
from unittest.mock import patch, MagicMock

# Import the module to test
from shivonai.lyra.crew_tools import crew_toolkit


class TestCrewIntegration(unittest.TestCase):
    """Test cases for CrewAI integration."""
    
    @patch('shivonai.core.mcp_client.MCPClient')
    def test_crew_toolkit(self, mock_client_class):
        """Test crew_toolkit function."""
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
        
        # Mock the CrewAI BaseTool import
        mock_base_tool = MagicMock()
        with patch('crewai.tools.BaseTool', mock_base_tool):
            # Call the function
            tools = crew_toolkit("test-token", "http://test-server:5000")
            
            # Assert
            mock_client_class.assert_called_once_with("http://test-server:5000")
            mock_client.authenticate.assert_called_once_with("test-token")
            mock_client.list_tools.assert_called_once()
            
            # Check that we got the expected tools
            self.assertEqual(len(tools), 1)
            
            # Check that BaseTool was subclassed correctly
            self.assertTrue(isinstance(tools[0].__class__, type))
            self.assertTrue(issubclass(tools[0].__class__, mock_base_tool))
    
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
        
        # Create a fake BaseTool class
        class FakeBaseTool:
            pass
        
        # Mock the CrewAI BaseTool import
        with patch('crewai.tools.BaseTool', FakeBaseTool):
            # Call the function to get the tools
            tools = crew_toolkit("test-token", "http://test-server:5000")
            
            # Get the first tool
            tool = tools[0]
            
            # Mock the _run method
            original_run = tool._run
            try:
                result = original_run('message=Hello, world!')
                
                # Assert
                mock_client.call_tool.assert_called_once_with("echo", {"message": "Hello, world!"})
                self.assertEqual(result, "Hello, world!")
            except Exception as e:
                self.fail(f"_run method raised an exception: {e}")


if __name__ == '__main__':
    unittest.main()