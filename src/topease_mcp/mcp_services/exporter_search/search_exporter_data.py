"""供应商企业查询 MCP 工具。"""

from __future__ import annotations

from typing import Any

from fastmcp import Context

from .exporterSearchServices import (
    ExporterDataService,
    ExporterQueryParams,
)
from topease_mcp.main import (
    TOPEASE_MCP_API_KEY,
    _format_error,
    _get_api_key_from_headers,
    mcp,
)
from topease_mcp.auth import validate_api_key

_exporter_service = ExporterDataService()


def _build_exporter_query_params(**kwargs: Any) -> ExporterQueryParams:
    """Build ExporterQueryParams from tool keyword arguments."""
    return ExporterQueryParams(
        prodesc=kwargs.get("prodesc"),
        hs_code=kwargs.get("hs_code"),
        country=kwargs.get("country"),
        company_name=kwargs.get("company_name"),
        to_country=kwargs.get("to_country"),
        recent_years=str(kwargs.get("recent_years", "1")),
        page_index=str(kwargs.get("page_index", "1")),
        page_size=str(kwargs.get("page_size", "10")),
        sort_field=kwargs.get("sort_field", "amount"),
        sort_type=kwargs.get("sort_type", "desc"),
    )


@mcp.tool(
    name="search_exporter_data",
    description=(
        "查询海关数据中的供应商企业。支持按产品关键字(prodesc)、"
        "HS编码(hs_code)、供应商企业名称(company_name)、"
        "企业所在国家(country)、销售目的国(to_country)、查询年份(recent_years)"
        "进行多维度联合查询。产品关键字、HS编码、供应商企业名称至少填一项。"
    ),
)
async def search_exporter_data(
    prodesc: str | None = None,
    hs_code: str | None = None,
    company_name: str | None = None,
    country: str | None = None,
    to_country: str | None = None,
    recent_years: str = "1",
    page_index: str = "1",
    page_size: str = "10",
    sort_field: str = "amount",
    sort_type: str = "desc",
    ctx: Context = Context,
) -> dict:
    """Query exporter enterprises from customs data with multiple filter dimensions.

    Args:
        prodesc: 产品关键字，例如 "LED"、"CABIN"。与 hs_code、company_name 至少填一项。
        hs_code: HS海关编码，例如 "8541"。与 prodesc、company_name 至少填一项。
        company_name: 供应商企业名称关键字。与 prodesc、hs_code 至少填一项。
        country: 企业所在国家（中文名/英文名/ISO编码均可），例如 "United States"、"中国"。
        to_country: 销售目的国，表示销售到哪个国家（中文名/英文名/ISO编码均可），值为 "United States" 表示销往美国。
        recent_years: 查询近几年的交易数据,最多支持近5年数据，默认 "1" 表示近一年。
        page_index: 页码，默认为 "1"。
        page_size: 每页记录数，默认为 "10"。
        sort_field: 排序字段，默认 "amount"（金额）。
        sort_type: 排序方向，"desc"（降序）或 "asc"（升序），默认 "desc"。

    Returns:
        JSON格式的查询结果，包含供应商企业列表和分页信息。
    """
    final_api_key = TOPEASE_MCP_API_KEY or _get_api_key_from_headers(ctx)

    if final_api_key == None:
        return _format_error(
            "API密钥缺失。请在请求头中传递 Authorization=Bearer <your_api_key> "
        )

    validate_api_key(final_api_key)
    _exporter_service.set_api_key(final_api_key)

    if not any([prodesc, hs_code, company_name]):
        return _format_error(
            "请至少提供一个查询条件："
            "产品关键字(prodesc)、HS编码(hs_code) 或 供应商企业名称(company_name)"
        )

    try:
        years = int(recent_years)
    except (ValueError, TypeError):
        return _format_error(
            f"recent_years 参数无效：'{recent_years}' 不是合法整数。请传入 1-5 之间的整数。"
        )

    if years < 1 or years > 5:
        return _format_error(
            f"recent_years 参数超出范围：{years}。最多支持近5年数据，请传入 1-5 之间的整数。"
        )

    params = _build_exporter_query_params(
        prodesc=prodesc,
        hs_code=hs_code,
        company_name=company_name,
        country=country,
        to_country=to_country,
        recent_years=recent_years,
        page_index=page_index,
        page_size=page_size,
        sort_field=sort_field,
        sort_type=sort_type,
    )

    result = await _exporter_service.search(params)
    return result
