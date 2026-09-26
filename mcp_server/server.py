"""MCP stdio entry point: python -m mcp_server.server."""

from mcp.server.fastmcp import FastMCP
from mcp_server.tools.configs import compare_configs
from mcp_server.tools.documentation import search_documentation
from mcp_server.tools.files import list_project_files, read_project_file
from mcp_server.tools.logs import analyze_logs

mcp = FastMCP("AI Engineering Assistant")
for tool in (
    analyze_logs, compare_configs, search_documentation,
    list_project_files, read_project_file,
):
    mcp.tool()(tool)

if __name__ == "__main__":
    mcp.run(transport="stdio")
