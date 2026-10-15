"""采购商企业查询 MCP 工具。"""

from __future__ import annotations

from typing import Any

from fastmcp import Context

from .importerSearchServices import (
    ImporterDataService,
    ImporterQueryParams,
)
from topease_mcp.main import (
    TOPEASE_MCP_API_KEY,
    _format_error,
    _get_api_key_from_headers,
    mcp,
)
from topease_mcp.auth import validate_api_key

_importer_service = ImporterDataService()


def _build_importer_query_params(**kwargs: Any) -> ImporterQueryParams:
    """Build ImporterQueryParams from tool keyword arguments."""
    return ImporterQueryParams(
        prodesc=kwargs.get("prodesc"),
        hs_code=kwargs.get("hs_code"),
        country=kwargs.get("country"),
        company_name=kwargs.get("company_name"),
        from_country=kwargs.get("from_country"),
        recent_years=str(kwargs.get("recent_years", "1")),
        page_index=str(kwargs.get("page_index", "1")),
        page_size=str(kwargs.get("page_size", "10")),
        sort_field=kwargs.get("sort_field", "amount"),
        sort_type=kwargs.get("sort_type", "desc"),
    )


@mcp.tool(
    name="search_importer_data",
    description=(
        "查询海关数据中的采购商企业。支持按产品关键字(prodesc)、"
        "HS编码(hs_code)、采购商企业名称(company_name)、"
        "企业所在国家(country)、采购来源国(from_country)、查询年份(recent_years)"
        "进行多维度联合查询。"
        "注意：产品关键字、HS编码、采购商企业名称其中至少填一项。"
    ),
)
async def search_importer_data(
    prodesc: str | None = None,
    hs_code: str | None = None,
    company_name: str | None = None,
    country: str | None = None,
    from_country: str | None = None,
    recent_years: str = "1",
    page_index: str = "1",
    page_size: str = "10",
    sort_field: str = "amount",
    sort_type: str = "desc",
    ctx: Context = Context,
) -> dict:
    """Query importer enterprises from customs data with multiple filter dimensions.

    Args:
        prodesc: 产品关键字，例如 "LED"、"CABIN"。与 hs_code、company_name 至少填一项。
        hs_code: HS海关编码，例如 "8541"。与 prodesc、company_name 至少填一项。
        company_name: 采购商企业名称关键字。与 prodesc、hs_code 至少填一项。
        country: 企业所在国家（中文名/英文名/ISO编码均可），例如 "United States"、"中国"。
        from_country: 采购来源国，表示从哪个国家采购过（中文名/英文名/ISO编码均可），值为 "China" 表示从中国采购。
        recent_years: 查询近几年的交易数据,最多支持近5年数据，默认 "1" 表示近一年。
        page_index: 页码，默认为 "1"。
        page_size: 每页记录数，默认为 "10"。
        sort_field: 排序字段，默认 "amount"（金额）。
        sort_type: 排序方向，"desc"（降序）或 "asc"（升序），默认 "desc"。

    Returns:
        JSON格式的查询结果，包含采购商企业列表和分页信息。
    """
    final_api_key = TOPEASE_MCP_API_KEY or _get_api_key_from_headers(ctx)

    if final_api_key == None:
        return _format_error(
            "API密钥缺失。请在请求头中传递 Authorization=Bearer <your_api_key> "
        )

    validate_api_key(final_api_key)
    _importer_service.set_api_key(final_api_key)

    if not any([prodesc, hs_code, company_name]):
        return _format_error(
            "请至少提供一个查询条件："
            "产品关键字(prodesc)、HS编码(hs_code) 或 采购商企业名称(company_name)"
        )

    params = _build_importer_query_params(
        prodesc=prodesc,
        hs_code=hs_code,
        company_name=company_name,
        country=country,
        from_country=from_country,
        recent_years=recent_years,
        page_index=page_index,
        page_size=page_size,
        sort_field=sort_field,
        sort_type=sort_type,
    )

    result = await _importer_service.search(params)
    return result
