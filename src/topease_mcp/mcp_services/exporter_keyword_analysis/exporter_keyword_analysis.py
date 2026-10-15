"""供应商贸易关键字分析 MCP 工具。"""

from __future__ import annotations

from typing import Any

from fastmcp import Context

from .exporterKeywordAnalysisServices import (
    ExporterKeywordAnalysisService,
    ExporterKeywordQueryParams,
)
from topease_mcp.main import (
    TOPEASE_MCP_API_KEY,
    _format_error,
    _get_api_key_from_headers,
    mcp,
)
from topease_mcp.auth import validate_api_key

_exporter_keyword_service = ExporterKeywordAnalysisService()


def _build_exporter_keyword_query_params(**kwargs: Any) -> ExporterKeywordQueryParams:
    """Build ExporterKeywordQueryParams from tool keyword arguments."""
    return ExporterKeywordQueryParams(
        t_code=kwargs.get("t_code", ""),
        page_index=str(kwargs.get("page_index", "1")),
        page_size=str(kwargs.get("page_size", "10")),
    )


@mcp.tool(
    name="exporter_keyword_analysis",
    description=(
        "查询指定供应商的贸易关键字统计分析。传入指定供应商企业ID（TCode），"
        "返回该供应商在贸易中涉及的关键字、对应贸易次数(count)及占比(countPercent)。"
    ),
)
async def exporter_keyword_analysis(
    t_code: str | None = None,
    page_index: str = "1",
    page_size: str = "10",
    ctx: Context = Context,
) -> dict:
    """Query trade keyword analysis for a specific exporter.

    Args:
        t_code: 供应商ID（TCode），必填。可通过 search_exporter_data 工具获取。
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
    _exporter_keyword_service.set_api_key(final_api_key)

    if not t_code:
        return _format_error(
            "请提供供应商ID（t_code 参数，即 TCode）。可先通过 search_exporter_data 工具查询供应商获取 TCode。"
        )

    params = _build_exporter_keyword_query_params(
        t_code=t_code,
        page_index=page_index,
        page_size=page_size,
    )

    result = await _exporter_keyword_service.search(params)
    return result
