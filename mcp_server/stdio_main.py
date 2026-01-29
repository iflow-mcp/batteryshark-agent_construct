"""
MCP Tool Server entry point for stdio transport.
"""
import asyncio
import logging
import os
from pathlib import Path
from mcp_server.core.server import MCPToolServer
from mcp_server.utils.logging_config import configure_logging
from mcp.server.stdio import stdio_server

async def main():
    """Run the MCP Tool Server with stdio transport."""
    # Configure logging first
    configure_logging()
    
    # Change to the script's directory to ensure correct path resolution
    script_dir = Path(__file__).parent.parent
    os.chdir(script_dir)
    logging.info(f"Working directory: {os.getcwd()}")
    
    # Initialize server - this will load tools
    server = MCPToolServer()
    
    # Log loaded tools for debugging
    logging.info(f"Loaded tools: {list(server.tool_manager.tools.keys())}")
    logging.info(f"Number of loaded tools: {len(server.tool_manager.tools)}")
    for name, tool_info in server.tool_manager.tools.items():
        logging.info(f"Tool: {name}, Desc: {tool_info.get('description', 'N/A')}")
    
    # Create initialization options
    init_options = server.app.create_initialization_options()
    
    # Run with stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server.app.run(
            read_stream,
            write_stream,
            init_options
        )

if __name__ == "__main__":
    asyncio.run(main())