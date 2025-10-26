import os
import asyncio
import subprocess
import time
from google.adk.tools.mcp_tool import McpToolset
from mcp.client.stdio import StdioServerParameters
API_SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api.py")
async def test_mcp_server():
    """Test the MCP server by checking tool availability."""
    # Connect to MCP server
    tools = McpToolset(
        connection_params=StdioServerParameters(
            command='python',
            args=[API_SCRIPT_PATH, '--mode', 'mcp']
        )
    )
    try:
        print("TOOLS",tools)
        # List available tools
        tool_names = [tool.name for tool in tools]
        print(f"Found {len(tool_names)} tools: {', '.join(tool_names)}")
        # Verify expected tools are available
        if "get_weather" in tool_names and "get_current_time" in tool_names:
            print("SUCCESS: MCP server is working correctly!")
        else:
            print("WARNING: Not all expected tools were found!")
    finally:
        pass

if __name__ == "__main__":
    asyncio.run(test_mcp_server())

