import os
import sys
import uvicorn
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
from dotenv import load_dotenv
from mcp import types as mcp_types
from mcp.server.lowlevel import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import json
import asyncio
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type
from google.adk.tools import AgentTool
from agents.agent import root_agent,injury_agent,insurance_agent,propertydmg_agent
from mcp.server.lowlevel import NotificationOptions
# Set up paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
AGENT_DIR = BASE_DIR  # Parent directory containing multi_tool_agent
# Set up DB path for sessions
SESSION_DB_URL = f"sqlite:///{os.path.join(BASE_DIR, 'sessions.db')}"
# Create the FastAPI app using ADK's helper
app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    session_db_kwargs=SESSION_DB_URL,
    allow_origins=["*"],  # In production, restrict this
    web=True,  # Enable the ADK Web UI
    
)

# Add custom endpoints
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
@app.get("/agent-info")
async def agent_info():
    """Provide agent information"""
    return {
        "agent_name": root_agent.name,
        "description": root_agent.description,
        "model": root_agent.model,
        # "tools": [t.__name__ for t in root_agent.tools]
    }



def create_mcp_server():
    """Creates an MCP server exposing our agent's tools."""
    # Create MCP Server
    app = Server("weather-time-mcp-server")

    @app.list_tools()
    async def list_tools() -> list[mcp_types.Tool]:
        """List available tools."""
        # Convert ADK tools to MCP format
        mcp_tools = [
            adk_to_mcp_tool_type(AgentTool(insurance_agent)),
            adk_to_mcp_tool_type(AgentTool(propertydmg_agent)),
            adk_to_mcp_tool_type(AgentTool(injury_agent)),
        ]
        return mcp_tools

    @app.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[mcp_types.TextContent]:
        """Execute a tool call."""
        # Map tool names to functions
        tools = {
            insurance_agent.name: insurance_agent,
            propertydmg_agent.name: propertydmg_agent,  
            injury_agent.name: injury_agent,
        }
        if name in tools:
            try:
                # Execute the tool
                result = await tools[name].run_async(
                    args=arguments,
                    tool_context=None,
                )
                return [mcp_types.TextContent(type="text", text=json.dumps(result))]
            except Exception as e:
                return [mcp_types.TextContent(
                    type="text", 
                    text=json.dumps({"error": str(e)})
                )]
        else:
            return [mcp_types.TextContent(
                type="text", 
                text=json.dumps({"error": f"Tool '{name}' not found"})
            )]
    return app
async def run_mcp_server():
    """Run the MCP server over standard I/O."""
    app = create_mcp_server()
    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name=app.name,
                    server_version="0.1.0",
                    capabilities=app.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    except Exception as e:
        logging.error(f"Failed to start MCP server: {e}")
        raise e  # Reraise the error so you can see it
import logging

logging.basicConfig(level=logging.DEBUG)
if __name__ == "__main__":
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="ADK Agent Server")
    parser.add_argument("--mode", choices=["web", "mcp"], default="web",
                      help="Run as web server or MCP server (default: web)")
    args = parser.parse_args()
    if args.mode == "mcp":
        # Run as MCP server
        print("Starting MCP server mode...")
        asyncio.run(run_mcp_server())
    else:
        # Run as web server (default)
        print("Starting Web server mode...")
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=9999, 
            reload=False
        )