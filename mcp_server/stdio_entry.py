"""
MCP Tool Server entry point for stdio transport.
"""
import asyncio
import logging
import os
import sys
from pathlib import Path
from mcp_server.core.server import MCPToolServer
from mcp_server.utils.logging_config import configure_logging
from mcp.server.stdio import stdio_server

def main():
    """Run the MCP Tool Server with stdio transport (synchronous entry point)."""
    # Configure logging first
    configure_logging()
    
    # Try to find the tools directory and set it as working directory
    # Check if we're running from an installed package
    if '__file__' in globals():
        # Running as a script
        script_path = Path(__file__).resolve()
        project_root = script_path.parent.parent
    else:
        # Running as an installed package, find the package location
        import mcp_server
        package_path = Path(mcp_server.__file__).resolve()
        project_root = package_path.parent.parent
    
    # Check if tools directory exists in project_root
    tools_dir = project_root / "tools"
    if not tools_dir.exists():
        # Try current directory
        tools_dir = Path.cwd() / "tools"
        if tools_dir.exists():
            project_root = Path.cwd()
    
    # Set working directory to where tools are located
    os.chdir(project_root)
    logging.info(f"Working directory: {os.getcwd()}")
    logging.info(f"Tools directory: {tools_dir}")
    
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
    asyncio.run(_async_main(server, init_options))

async def _async_main(server, init_options):
    """Async main function."""
    async with stdio_server() as (read_stream, write_stream):
        await server.app.run(
            read_stream,
            write_stream,
            init_options
        )

if __name__ == "__main__":
    main()