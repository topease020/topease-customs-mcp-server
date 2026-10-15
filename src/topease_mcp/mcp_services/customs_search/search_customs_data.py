"""海关贸易数据查询 MCP 工具。"""

from __future__ import annotations

from typing import Any

from fastmcp import Context

from .TradeSearchServices import (
    CustomsDataService,
    CustomsQueryParams,
    TradeType,
)
from topease_mcp.main import (
    TOPEASE_MCP_API_KEY,
    _format_error,
    _get_api_key_from_headers,
    mcp,
)
from topease_mcp.auth import validate_api_key

_customs_service = CustomsDataService()


def _build_query_params(**kwargs: Any) -> CustomsQueryParams:
    """Build CustomsQueryParams from tool keyword arguments."""
    print(TradeType(kwargs.get("trade_type", "all")))
    return CustomsQueryParams(
        product_keyword=kwargs.get("product_keyword"),
        hs_code=kwargs.get("hs_code"),
        company_name=kwargs.get("company_name"),
        trade_type=TradeType(kwargs.get("trade_type", "all")),
        country=kwargs.get("country"),
        date_from=kwargs.get("date_from"),
        date_to=kwargs.get("date_to"),
        page_index=kwargs.get("page_index", 1),
        page_size=kwargs.get("page_size", 20),
        sort_by=kwargs.get("sort_by", "tradedate"),
        sort_order=kwargs.get("sort_order", "desc"),
    )


@mcp.tool(
    name="search_customs_data",
    description=(
        "查询海关贸易明细数据。支持按企业名称(company_name)、"
        "产品关键字(product_keyword)、HS编码(hs_code)、"
        "贸易时间(date_from/date_to)、进出口类型(trade_type)及"
        "原产国(country)进行多维度联合查询。"
        "注意：企业名称、产品关键字及HS编码其中至少一个必填项。"
    ),
)
async def search_customs_data(
    company_name: str | None = None,
    product_keyword: str | None = None,
    hs_code: str | None = None,
    trade_type: str = "all",
    country: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    page_index: int = 1,
    page_size: int = 20,
    sort_by: str = "tradedate",
    sort_order: str = "desc",
    ctx: Context = Context,
) -> dict:
    """Query customs trade data with multiple filter dimensions.

    Args:
        company_name: 企业名称（模糊匹配进口商/出口商名称），会做后置过滤。
        product_keyword: 产品描述关键字，例如 "CABIN"、"VALVE"。
        hs_code: HS海关编码（前缀匹配），例如 "8415"。
        trade_type: 贸易类型：import(进口)、export(出口)、all(全部，默认)。
        country: 数据源国（英文名），例如 "Japan"、"China"。
        date_from: 贸易起始日期，格式 YYYY-MM-DD。默认 2025-01-01。
        date_to: 贸易结束日期，格式 YYYY-MM-DD。默认当前时间。
        page_index: 页码，默认为1。
        page_size: 每页记录数，默认为20，最大100。
        sort_by: 排序字段，默认 tradedate。支持排序字段；tradedate,quantity,weight,uusd
        sort_order: 排序方向，asc/desc，默认 desc。

    Returns:
        JSON格式的查询结果，包含记录列表和分页信息。
    """
    print("------------TOPEASE_MCP_API_KEY")
    print(TOPEASE_MCP_API_KEY)

    final_api_key = TOPEASE_MCP_API_KEY or _get_api_key_from_headers(ctx)

    if final_api_key == None:
        return _format_error(
            "API密钥缺失。请在请求头中传递 Authorization=Bearer <your_api_key> "
        )

    validate_api_key(final_api_key)
    _customs_service.set_api_key(final_api_key)

    if not any([company_name, product_keyword, hs_code, country]):
        return _format_error(
            "请至少提供一个查询条件："
            "企业名称(company_name)、产品关键字(product_keyword)、"
            "HS编码(hs_code) 或 原产国(country)"
        )

    params = _build_query_params(
        product_keyword=product_keyword,
        hs_code=hs_code,
        company_name=company_name,
        trade_type=trade_type,
        country=country,
        date_from=date_from,
        date_to=date_to,
        page_index=page_index,
        page_size=min(page_size, 20),
        sort_by=sort_by,
        sort_order=sort_order,
    )

    result = await _customs_service.search(params)
    return result
