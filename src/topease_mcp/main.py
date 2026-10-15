"""MCP server for customs trade data query.

Provides tools for querying customs trade data with mandatory
API key authentication. Third-party LLMs MUST provide a valid API_KEY
to access any tool on this server.

Real API: POST https://api.topease.net/api/search_trade

API Key Authentication:
    When using streamable-http protocol, API key should be passed in 
    Authorization header: Authorization=Bearer <your_api_key>

Usage:
    # Streamable HTTP mode (for Claude Desktop, Trae, etc.)
    python -m topease_mcp
    # or
    uvicorn server:app --host 0.0.0.0 --port 8001
"""

from __future__ import annotations

import os

from typing import Any, Optional

from dotenv import load_dotenv
from fastmcp import FastMCP, Context
from starlette.requests import Request
from topease_mcp.setting import PORT

load_dotenv()

TOPEASE_MCP_API_KEY = os.getenv("TOPEASE_MCP_API_KEY")

mcp = FastMCP(
    name="topease-customs-data",
    instructions=(
        "topease-customs-data MCP 提供全球海关贸易数据查询/分析服务。"
    ),
)


def _format_error(message: str) -> dict[str, Any]:
    return {"data": [], "message": message, "code": 400}


# ──────────────────────────────────────────────
# Shared helpers
# ──────────────────────────────────────────────


def _get_api_key_from_headers(ctx: Context) -> Optional[str]:
    """Extract API key from Authorization header.

    Args:
        ctx: FastMCP Context object containing request information.

    Returns:
        The API key string if found and valid, None otherwise.
    """
    # 1. 检查上下文和请求对象是否存在
    if not ctx or not ctx.request_context or not ctx.request_context.request:
        return None

    # 2. 验证请求对象类型
    request = ctx.request_context.request
    if not isinstance(request, Request):
        return None

    # 3. 获取 headers（保留原始 Headers 对象，使用 get 方法避免 KeyError）
    headers = request.headers

    # 4. 检查 authorization 是否存在（大小写不敏感）
    auth_header = headers.get("Authorization") or headers.get("authorization")
    print("------------auth_header")
    print(auth_header)
    if not auth_header:
        return None  # authorization 不存在，返回 None

    # 5. 从 Bearer 格式中提取 API key
    if auth_header.startswith("Bearer "):
        api_key = auth_header[7:].strip()
        return api_key if api_key else None

    # 6. 支持 Token 格式
    if auth_header.startswith("Token "):
        api_key = auth_header[6:].strip()
        return api_key if api_key else None

    # 7. 其他格式或无效授权
    return None


# ──────────────────────────────────────────────
# Import tool modules to register MCP tools
# ──────────────────────────────────────────────

from topease_mcp.mcp_services.customs_search.search_customs_data import *  # noqa: F401,E402
from topease_mcp.mcp_services.importer_search.search_importer_data import *  # noqa: F401,E402
from topease_mcp.mcp_services.exporter_search.search_exporter_data import *  # noqa: F401,E402
from topease_mcp.mcp_services.importer_keyword_analysis.importer_keyword_analysis import *  # noqa: F401,E402
from topease_mcp.mcp_services.importer_role_analysis.importer_role_analysis import *  # noqa: F401,E402
from topease_mcp.mcp_services.importer_hscode_analysis.importer_hscode_analysis import *  # noqa: F401,E402
from topease_mcp.mcp_services.importer_port_analysis.importer_port_analysis import *  # noqa: F401,E402
from topease_mcp.mcp_services.importer_cycle_analysis.importer_cycle_analysis import *  # noqa: F401,E402
from topease_mcp.mcp_services.importer_exporter_analysis.importer_exporter_analysis import *  # noqa: F401,E402
from topease_mcp.mcp_services.exporter_keyword_analysis.exporter_keyword_analysis import *  # noqa: F401,E402
from topease_mcp.mcp_services.exporter_role_analysis.exporter_role_analysis import *  # noqa: F401,E402
from topease_mcp.mcp_services.exporter_hscode_analysis.exporter_hscode_analysis import *  # noqa: F401,E402
from topease_mcp.mcp_services.exporter_port_analysis.exporter_port_analysis import *  # noqa: F401,E402
from topease_mcp.mcp_services.exporter_cycle_analysis.exporter_cycle_analysis import *  # noqa: F401,E402
from topease_mcp.mcp_services.exporter_importer_analysis.exporter_importer_analysis import *  # noqa: F401,E402


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────


def main() -> None:
    """Run the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
