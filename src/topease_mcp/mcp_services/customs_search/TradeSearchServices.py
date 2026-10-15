from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import requests
import json
from dotenv import load_dotenv
from topease_mcp.country import find_by_id, find_country
from topease_mcp.setting import BASE_URL

load_dotenv()

class TradeType(str, Enum):
    IMPORT = "import"
    EXPORT = "export"
    ALL = "all"

    def to_ie(self) -> int:
        """将贸易类型映射为 ie 整数值: import→1, export→0, all→2"""
        mapping = {
            TradeType.IMPORT: 1,
            TradeType.EXPORT: 0,
            TradeType.ALL: 2,
        }
        return mapping[self]


@dataclass
class CustomsRecord:
    """A single customs trade record matching the real API response."""

    bill_id: str = ""
    country_id: int = 0
    ie: int = 0
    hs_code: str = ""
    prodesc: str = ""
    importer_name: str = ""
    exporter_name: str = ""
    quantity: float = 0.0
    weight: float = 0.0
    trade_date: str = ""
    amount_usd: float = 0.0
    quantity_unit: str = ""
    origin_country: str = ""

    @property
    def trade_type(self) -> str:
        return "进口" if self.ie == 1 else "出口"

    @property
    def company_name(self) -> str:
        return self.importer_name if self.ie == 1 else self.exporter_name

    def to_dict(self) -> dict[str, Any]:
        return {
            "单据ID": self.bill_id,
            "海关编码": self.hs_code,
            "产品描述": self.prodesc,
            "贸易类型": self.trade_type,
            "进口商": self.importer_name,
            "出口商": self.exporter_name,
            "数量": self.quantity,
            "数量单位": self.quantity_unit,
            "重量": self.weight,
            "金额(USD)": round(self.amount_usd, 4),
            "贸易日期": self.trade_date,
            "原产国": self.origin_country,
            "原产国ID": self.country_id,
        }


@dataclass
class CustomsQueryParams:
    """Parameters for customs data search, mapped to the real API."""

    product_keyword: str | None = None
    hs_code: str | None = None
    company_name: str | None = None
    trade_type: TradeType = TradeType.ALL
    country: str | None = None
    date_from: str | None = None
    date_to: str | None = None
    page_index: int = 1
    page_size: int = 20
    sort_by: str = "tradedate"
    sort_order: str = "desc"

    def to_api_body(self) -> dict[str, Any]:
        """Build the JSON request body for the real API."""

        country_id = 0
        if self.country:
            resolved_id = find_country(self.country)
            if resolved_id is not None:
                country_id = resolved_id

        body: dict[str, Any] = {
            "pageSize": (self.page_size),
            "countryId": country_id,
            "ie": self.trade_type.to_ie(),
            "pageIndex": (self.page_index),
            "sortType": self.sort_order,
            "sortField": self.sort_by,
            "prodesc": self.product_keyword or "",
            "hsCode": self.hs_code or "",
            "companyName": self.company_name or "",
            "bDate": self.date_from or "",
            "eDate": self.date_to or "",
        }
        return body


@dataclass
class CustomsQueryResult:
    """Search result containing records and pagination info."""

    records: list[CustomsRecord] = field(default_factory=list)
    total: int = 0
    page_index: int = 1
    page_size: int = 20
    total_pages: int = 0
    code: int = 200
    message: str = ""
    query_params: CustomsQueryParams | None = None

    @property
    def has_more(self) -> bool:
        return self.page_index < self.total_pages



class CustomsDataService:

    def __init__(self, base_url: str | None = None, timeout: float = 30.0):
        self._base_url = base_url or BASE_URL
        self._timeout = timeout
        self._api_key: str | None = None

    def set_api_key(self, api_key: str) -> None:
        """Set the API key for authentication."""
        self._api_key = api_key

    async def search(self, params: CustomsQueryParams) -> CustomsQueryResult:
        # try:
        return await self._search_api(params)
        # except Exception:
        #     return self._search_mock(params)

    async def _search_api(self, params: CustomsQueryParams) -> CustomsQueryResult:
        body = params.to_api_body()
        print("==================body")
        print(body)
        headers: dict[str, str] = {}
        headers["Content-Type"] = "application/json"
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        url = BASE_URL + "/trade_search"

        response = requests.request("POST", url, headers=headers, data=json.dumps(params.to_api_body()))
        print("==================response-----",url)
        print(response.json())
        print(headers)
        data = response.json().get("data", {})
        if (response.json().get("code")!=200):
            return CustomsQueryResult(               
                code=response.json().get("code"),
                message=response.json().get("message", ""),
            )
        
        items = data.get("result", [])
        for item in items:
            ie_val = item.get("ie", 0)
            if ie_val == 0:
                item["trade_type"] = "export"
            elif ie_val == 1:
                item["trade_type"] = "import"

            country_id = item.get("countryId", 0)
            if country_id:
                country_info = find_by_id(country_id)
                if country_info:
                    item["countryCnName"] = country_info["name"]
                    item["countryName"] = country_info["enName"]
                    # item["country_code2"] = country_info["code2"]
                    # item["country_code3"] = country_info["code3"]

        total = data.get("total", len(items))
        page_size = int(data.get("pageSize", params.page_size))
        page_index = int(data.get("pageIndex", params.page_index))
        total_pages = max(1, (total + page_size - 1) // page_size)

        result = CustomsQueryResult(
            records=items,
            total=total,
            page_index=page_index,
            page_size=page_size,
            total_pages=total_pages,
            query_params=params,
        )
        return result
