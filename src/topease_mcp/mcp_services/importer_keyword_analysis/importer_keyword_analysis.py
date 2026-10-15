"""采购商贸易关键字分析 MCP 工具。"""

from __future__ import annotations

from typing import Any

from fastmcp import Context

from .importerKeywordAnalysisServices import (
    ImporterKeywordAnalysisService,
    ImporterKeywordQueryParams,
)
from topease_mcp.main import (
    TOPEASE_MCP_API_KEY,
    _format_error,
    _get_api_key_from_headers,
    mcp,
)
from topease_mcp.auth import validate_api_key

_importer_keyword_service = ImporterKeywordAnalysisService()


def _build_importer_keyword_query_params(**kwargs: Any) -> ImporterKeywordQueryParams:
    """Build ImporterKeywordQueryParams from tool keyword arguments."""
    return ImporterKeywordQueryParams(
        t_code=kwargs.get("t_code", ""),
        page_index=str(kwargs.get("page_index", "1")),
        page_size=str(kwargs.get("page_size", "10")),
    )


@mcp.tool(
    name="importer_keyword_analysis",
    description=(
        "查询指定采购商的贸易关键字统计分析。传入指定采购商企业ID（TCode），"
        "返回该采购商在贸易中涉及的关键字、对应贸易次数(count)及占比(countPercent)。"
    ),
)
async def importer_keyword_analysis(
    t_code: str | None = None,
    page_index: str = "1",
    page_size: str = "10",
    ctx: Context = Context,
) -> dict:
    """Query trade keyword analysis for a specific importer.

    Args:
        t_code: 采购商ID（TCode），必填。可通过 search_importer_data 工具获取。
        page_index: 页码，默认为 "1"。
        page_size: 每页记录数，默认为 "10"。

    Returns:
        JSON格式的查询结果，包含贸易关键字列表（keyword、count、countPercent）和分页信息。
    """
    final_api_key = TOPEASE_MCP_API_KEY or _get_api_key_from_headers(ctx)

    if final_api_key == None:
        return _format_error(
            "API密钥缺失。请在请求头中传递 Authorization=Bearer <your_api_key> "
        )

    validate_api_key(final_api_key)
    _importer_keyword_service.set_api_key(final_api_key)

    if not t_code:
        return _format_error(
            "请提供采购商ID（t_code 参数，即 TCode）。可先通过 search_importer_data 工具查询采购商获取 TCode。"
        )

    params = _build_importer_keyword_query_params(
        t_code=t_code,
        page_index=page_index,
        page_size=page_size,
    )

    result = await _importer_keyword_service.search(params)
    return result
