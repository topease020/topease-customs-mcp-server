"""供应商贸易趋势分析 MCP 工具。"""

from __future__ import annotations

from typing import Any

from fastmcp import Context

from .exporterCycleAnalysisServices import (
    ExporterCycleAnalysisService,
    ExporterCycleQueryParams,
)
from topease_mcp.main import (
    TOPEASE_MCP_API_KEY,
    _format_error,
    _get_api_key_from_headers,
    mcp,
)
from topease_mcp.auth import validate_api_key

_exporter_cycle_service = ExporterCycleAnalysisService()


def _build_exporter_cycle_query_params(**kwargs: Any) -> ExporterCycleQueryParams:
    """Build ExporterCycleQueryParams from tool keyword arguments."""
    return ExporterCycleQueryParams(
        t_code=kwargs.get("t_code", ""),
        hs_code=kwargs.get("hs_code"),
        prodesc=kwargs.get("prodesc"),
        b_date=kwargs.get("b_date"),
        e_date=kwargs.get("e_date"),
        page_index=str(kwargs.get("page_index", "1")),
        page_size=str(kwargs.get("page_size", "12")),
        sort_field=kwargs.get("sort_field", "tradeDate"),
        sort_type=kwargs.get("sort_type", "desc"),
    )


@mcp.tool(
    name="exporter_cycle_analysis",
    description=(
        "查询指定供应商的贸易趋势（按月统计）。传入供应商ID（TCode），"
        "按月返回该供应商的贸易次数(count)、贸易金额(amount)、数量(quantity)、"
        "重量(weight)、箱量(teus)，可用于观察供应商的贸易季节性和周期性变化。"
    ),
)
async def exporter_cycle_analysis(
    t_code: str | None = None,
    hs_code: str | None = None,
    prodesc: str | None = None,
    b_date: str | None = None,
    e_date: str | None = None,
    page_index: str = "1",
    page_size: str = "12",
    sort_field: str = "tradeDate",
    sort_type: str = "desc",
    ctx: Context = Context,
) -> dict:
    """Query trade cycle analysis (monthly trend) for a specific exporter.

    Args:
        t_code: 供应商ID（TCode），必填。可通过 search_exporter_data 工具获取。
        hs_code: HS 编码前缀过滤。
        prodesc: 提单描述关键字，用于进一步过滤结果。
        b_date: 交易起始日期，格式 yyyy-MM-dd。
        e_date: 交易结束日期，格式 yyyy-MM-dd。
        page_index: 页码，默认为 "1"。
        page_size: 每页记录数，默认为 "12"（对应 12 个月）。
        sort_field: 排序字段，默认为 "tradeDate"。可选值：tradeDate、quantity、weight、amount、count。
        sort_type: 排序方式，"desc"（降序）或 "asc"（升序），默认 "desc"。

    Returns:
        JSON格式的查询结果，包含按月统计列表（tradeDate、count、amount、quantity、weight、teus）和分页信息。
    """
    final_api_key = TOPEASE_MCP_API_KEY or _get_api_key_from_headers(ctx)

    if final_api_key == None:
        return _format_error(
            "API密钥缺失。请在请求头中传递 Authorization=Bearer <your_api_key> "
        )

    validate_api_key(final_api_key)
    _exporter_cycle_service.set_api_key(final_api_key)

    if not t_code:
        return _format_error(
            "请提供供应商ID（t_code 参数，即 TCode）。可先通过 search_exporter_data 工具查询供应商获取 TCode。"
        )

    params = _build_exporter_cycle_query_params(
        t_code=t_code,
        hs_code=hs_code,
        prodesc=prodesc,
        b_date=b_date,
        e_date=e_date,
        page_index=page_index,
        page_size=page_size,
        sort_field=sort_field,
        sort_type=sort_type,
    )

    result = await _exporter_cycle_service.search(params)
    return result
