"""采购商贸易角色分析 MCP 工具。"""

from __future__ import annotations

from typing import Any

from fastmcp import Context

from .importerRoleAnalysisServices import (
    ImporterRoleAnalysisService,
    ImporterRoleQueryParams,
)
from topease_mcp.main import (
    TOPEASE_MCP_API_KEY,
    _format_error,
    _get_api_key_from_headers,
    mcp,
)
from topease_mcp.auth import validate_api_key

_importer_role_service = ImporterRoleAnalysisService()


def _build_importer_role_query_params(**kwargs: Any) -> ImporterRoleQueryParams:
    """Build ImporterRoleQueryParams from tool keyword arguments."""
    return ImporterRoleQueryParams(
        t_code=kwargs.get("t_code", ""),
        sort_field=kwargs.get("sort_field", "amount"),
        sort_type=kwargs.get("sort_type", "desc"),
    )


@mcp.tool(
    name="importer_role_analysis",
    description=(
        "查询指定采购商的贸易角色统计分析。传入指定采购商企业ID（TCode），"
        "返回该采购商的贸易角色（role，如采购商/供应商）、数据源国家、数据源类型（进口/出口）、"
        "贸易总金额、贸易次数及对应的金额/次数占比。"
    ),
)
async def importer_role_analysis(
    t_code: str | None = None,
    sort_field: str = "amount",
    sort_type: str = "desc",
    ctx: Context = Context,
) -> dict:
    """Query trade role analysis for a specific importer.

    Args:
        t_code: 采购商ID（TCode），必填。可通过 search_importer_data 工具获取。
        sort_field: 排序字段，默认为 "amount"。可选值：quantity、weight、amount、count。
        sort_type: 排序方式，"desc"（降序）或 "asc"（升序），默认 "desc"。

    Returns:
        JSON格式的查询结果，包含贸易角色列表（role、dataSourceCountry、dataSourceType、
        amount、count、amountPercent、countPercent）和分页信息。
    """
    final_api_key = TOPEASE_MCP_API_KEY or _get_api_key_from_headers(ctx)

    if final_api_key == None:
        return _format_error(
            "API密钥缺失。请在请求头中传递 Authorization=Bearer <your_api_key> "
        )

    validate_api_key(final_api_key)
    _importer_role_service.set_api_key(final_api_key)

    if not t_code:
        return _format_error(
            "请提供采购商ID（t_code 参数，即 TCode）。可先通过 search_importer_data 工具查询采购商获取 TCode。"
        )

    params = _build_importer_role_query_params(
        t_code=t_code,
        sort_field=sort_field,
        sort_type=sort_type,
    )

    result = await _importer_role_service.search(params)
    return result
