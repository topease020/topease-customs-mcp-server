"""供应商企业搜索模块。

提供海关数据中供应商企业的查询功能，支持按产品关键字、HS编码、
企业名称、国家等多维度检索供应商信息。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import requests
import json

from topease_mcp.country import find_by_id, find_country
from topease_mcp.setting import BASE_URL


@dataclass
class ExporterQueryParams:
    """供应商查询参数，映射到 exporter_search API。"""

    prodesc: str | None = None
    hs_code: str | None = None
    country: str | None = None
    company_name: str | None = None
    to_country: str | None = None
    recent_years: str = "1"
    page_index: str = "1"
    page_size: str = "10"
    sort_field: str = "amount"
    sort_type: str = "desc"

    def to_api_body(self) -> dict[str, Any]:
        """构建 API 请求体。"""
        country_id = ""
        if self.country:
            resolved_id = find_country(self.country)
            if resolved_id is not None:
                country_id = str(resolved_id)

        to_country_id = ""
        if self.to_country:
            resolved_id = find_country(self.to_country)
            if resolved_id is not None:
                to_country_id = str(resolved_id)

        body: dict[str, Any] = {
            "prodesc": self.prodesc or "",
            "hsCode": self.hs_code or "",
            "countryId": country_id,
            "companyName": self.company_name or "",
            "toCountryId": to_country_id,
            "recentYears": self.recent_years,
            "pageIndex": self.page_index,
            "pageSize": self.page_size,
            "sortField": self.sort_field,
            "sortType": self.sort_type,
        }
        return body


@dataclass
class ExporterQueryResult:
    """供应商查询结果，包含记录列表和分页信息。

    分页字段（来自 API 响应 data 对象）:
        total     (int) 符合条件的总记录数（总行数）
        page_size (int) 每页显示条数（API: data.pageSize）
        page_index (int) 当前分页索引（API: data.pageIndex）

    records 列表元素字段（每个 dict 对应接口文档"返回数据"中的 result[i]，均为必须字段）:
        TCode          (Encryption) 供应商Tcode          ← records[i]["TCode"]
        name           (String)     企业名称            ← records[i]["name"]
        countryId      (Long)       企业所在国家ID      ← records[i]["countryId"]
        relatedCount   (Long)       相关交易单数        ← records[i]["relatedCount"]
        totalCount     (Long)       总交易单数          ← records[i]["totalCount"]
        maxTradeDate   (String)     企业最近贸易时间    ← records[i]["maxTradeDate"]
        relatedProduct (String)     关联产品描述        ← records[i]["relatedProduct"]
        relatedHsCode  (String)     关联产品编码        ← records[i]["relatedHsCode"]

    服务层附加注入的国家名称字段（根据 ID 解析，非 API 原始返回）:
        countryCnName    (String) 企业所在国家中文名
        countryName      (String) 企业所在国家英文名
        toCountryCnName  (String) 销售目的国中文名
        toCountryName    (String) 销售目的国英文名
    """

    # 供应商企业列表，每个元素为 dict，字段含义见上方 docstring
    records: list[dict[str, Any]] = field(default_factory=list)  # 元素字段: TCode, name, countryId, relatedCount, totalCount, maxTradeDate, relatedProduct, relatedHsCode
    total: int = 0       # 符合条件的总条数（API: data.total）
    page_index: int = 1  # 当前分页索引（API: data.pageIndex）
    page_size: int = 10  # 每页显示条数（API: data.pageSize）
    total_pages: int = 0  # 总页数 = ceil(total / page_size)
    code: int = 200
    message: str = ""
    query_params: ExporterQueryParams | None = None  # 原始查询参数，用于翻页或排查

    @property
    def has_more(self) -> bool:
        return self.page_index < self.total_pages


class ExporterDataService:
    """供应商数据服务，封装 exporter_search API 调用。"""

    def __init__(self, base_url: str | None = None, timeout: float = 30.0):
        self._base_url = base_url or BASE_URL
        self._timeout = timeout
        self._api_key: str | None = None

    def set_api_key(self, api_key: str) -> None:
        """设置 API Key 用于鉴权。"""
        self._api_key = api_key

    async def search(self, params: ExporterQueryParams) -> ExporterQueryResult:
        """执行供应商搜索。"""
        return await self._search_api(params)

    async def _search_api(self, params: ExporterQueryParams) -> ExporterQueryResult:
        body = params.to_api_body()
        print("==================exporter body")
        print(body)

        headers: dict[str, str] = {}
        headers["Content-Type"] = "application/json"
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        url = BASE_URL + "/exporter_search"

        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(body)
        )

        
        data = response.json().get("data", {})
        if (response.json().get("code")!=200):
            return ExporterQueryResult(               
                code=response.json().get("code"),
                message=response.json().get("message", ""),
            )
        
        items = data.get("result", [])

        for item in items:
            # 解析国家信息
            country_id = item.get("countryId", 0)
            if country_id:
                country_info = find_by_id(country_id)
                if country_info:
                    item["countryCnName"] = country_info["name"]
                    item["countryName"] = country_info["enName"]

            # 解析销售目的国信息
            to_country_id = item.get("toCountryId", 0)
            if to_country_id:
                to_country_info = find_by_id(to_country_id)
                if to_country_info:
                    item["toCountryCnName"] = to_country_info["name"]
                    item["toCountryName"] = to_country_info["enName"]

        total = data.get("total", len(items))
        page_size = int(data.get("pageSize", params.page_size))
        page_index = int(data.get("pageIndex", params.page_index))
        total_pages = max(1, (total + page_size - 1) // page_size)

        result = ExporterQueryResult(
            records=items,
            total=total,
            page_index=page_index,
            page_size=page_size,
            total_pages=total_pages,
            query_params=params,
        )
        return result
