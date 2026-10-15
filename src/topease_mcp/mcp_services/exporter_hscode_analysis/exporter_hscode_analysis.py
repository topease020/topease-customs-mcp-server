"""供应商贸易编码分析 MCP 工具。"""

from __future__ import annotations

from typing import Any

from fastmcp import Context

from .exporterHsCodeAnalysisServices import (
    ExporterHsCodeAnalysisService,
    ExporterHsCodeQueryParams,
)
from topease_mcp.main import (
    TOPEASE_MCP_API_KEY,
    _format_error,
    _get_api_key_from_headers,
    mcp,
)
from topease_mcp.auth import validate_api_key

_exporter_hscode_service = ExporterHsCodeAnalysisService()


def _build_exporter_hscode_query_params(**kwargs: Any) -> ExporterHsCodeQueryParams:
    """Build ExporterHsCodeQueryParams from tool keyword arguments."""
    return ExporterHsCodeQueryParams(
        t_code=kwargs.get("t_code", ""),
        prodesc=kwargs.get("prodesc"),
        hs_code=kwargs.get("hs_code"),
        b_date=kwargs.get("b_date"),
        e_date=kwargs.get("e_date"),
        page_index=str(kwargs.get("page_index", "1")),
        page_size=str(kwargs.get("page_size", "10")),
        sort_field=kwargs.get("sort_field", "amount"),
        sort_type=kwargs.get("sort_type", "desc"),
    )


@mcp.tool(
    name="exporter_hscode_analysis",
    description=(
        "查询指定供应商的贸易编码（HS Code）统计分析。传入供应商ID（TCode），"
        "返回该供应商的HS编码、贸易次数(count)、贸易金额(amount)、数量(quantity)、"
        "重量(weight)、箱量(teus)及各维度对应的占比，同时包含中文/英文海关编码描述。"
    ),
)
async def exporter_hscode_analysis(
    t_code: str | None = None,
    prodesc: str | None = None,
    hs_code: str | None = None,
    b_date: str | None = None,
    e_date: str | None = None,
    page_index: str = "1",
    page_size: str = "10",
    sort_field: str = "amount",
    sort_type: str = "desc",
    ctx: Context = Context,
) -> dict:
    """Query HS Code analysis for a specific exporter.

    Args:
        t_code: 供应商ID（TCode），必填。可通过 search_exporter_data 工具获取。
        prodesc: 提单描述关键字，用于进一步过滤结果。
        hs_code: HS 编码前缀过滤。
        b_date: 交易起始日期，格式 yyyy-MM-dd。
        e_date: 交易结束日期，格式 yyyy-MM-dd。
        page_index: 页码，默认为 "1"。
        page_size: 每页记录数，默认为 "10"。
        sort_field: 排序字段，默认为 "amount"。可选值：quantity、weight、amount、count、teus。
        sort_type: 排序方式，"desc"（降序）或 "asc"（升序），默认 "desc"。

    Returns:
        JSON格式的查询结果，包含HS编码列表（hsCode、count、amount、quantity、weight、teus、
        各维度占比、cnDescription、enDescription）和分页信息。
    """
    final_api_key = TOPEASE_MCP_API_KEY or _get_api_key_from_headers(ctx)

    if final_api_key == None:
        return _format_error(
            "API密钥缺失。请在请求头中传递 Authorization=Bearer <your_api_key> "
        )

    validate_api_key(final_api_key)
    _exporter_hscode_service.set_api_key(final_api_key)

    if not t_code:
        return _format_error(
            "请提供供应商ID（t_code 参数，即 TCode）。可先通过 search_exporter_data 工具查询供应商获取 TCode。"
        )

    params = _build_exporter_hscode_query_params(
        t_code=t_code,
        prodesc=prodesc,
        hs_code=hs_code,
        b_date=b_date,
        e_date=e_date,
        page_index=page_index,
        page_size=page_size,
        sort_field=sort_field,
        sort_type=sort_type,
    )

    result = await _exporter_hscode_service.search(params)
    return result
