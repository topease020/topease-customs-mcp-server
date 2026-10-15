"""采购商贸易趋势分析模块。

根据采购商ID（TCode）查询该采购商的贸易趋势（按月统计），
包含贸易次数/金额/数量/重量/箱量按月汇总。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import requests
import json

from topease_mcp.setting import BASE_URL


@dataclass
class ImporterCycleQueryParams:
    """采购商贸易趋势查询参数，映射到 importer_cycle_analysis API。"""

    t_code: str  # 采购商TCode（必填）
    hs_code: str | None = None
    prodesc: str | None = None
    b_date: str | None = None
    e_date: str | None = None
    page_index: str = "1"
    page_size: str = "12"  # 默认每页12条（对应12个月）
    sort_field: str = "tradeDate"
    sort_type: str = "desc"

    def to_api_body(self) -> dict[str, Any]:
        """构建 API 请求体。"""
        body: dict[str, Any] = {
            "TCode": self.t_code,
            "hsCode": self.hs_code or "",
            "prodesc": self.prodesc or "",
            "bDate": self.b_date or "",
            "eDate": self.e_date or "",
            "pageIndex": self.page_index,
            "pageSize": self.page_size,
            "sortField": self.sort_field,
            "sortType": self.sort_type,
        }
        return body


@dataclass
class ImporterCycleQueryResult:
    """采购商贸易趋势查询结果，包含记录列表和分页信息。    
    
    分页字段（来自 API 响应 data 对象）:
        total     (int) 符合条件的总记录数（总行数）
        page_size (int) 每页显示条数（API: data.pageSize）
        page_index (int) 当前分页索引（API: data.pageIndex）

    records 列表元素字段（每个 dict 对应接口文档"返回数据"中的 result[i]，均为必须字段）:
        tradeDate (String)  交易月份          ← records[i]["tradeDate"]
        teus      (Decimal) 贸易总箱量        ← records[i]["teus"]
        count     (Long)    贸易次数          ← records[i]["count"]
        amount    (Decimal) 贸易总金额        ← records[i]["amount"]
        quantity  (Decimal) 贸易总数量        ← records[i]["quantity"]
        weight    (Decimal) 贸易总重量        ← records[i]["weight"]
    """

    records: list[dict[str, Any]] = field(default_factory=list)
    total: int = 0
    page_index: int = 1
    page_size: int = 12
    total_pages: int = 0
    code: int = 200
    message: str = ""
    query_params: ImporterCycleQueryParams | None = None

    @property
    def has_more(self) -> bool:
        return self.page_index < self.total_pages


class ImporterCycleAnalysisService:
    """采购商贸易趋势分析服务，封装 importer_cycle_analysis API 调用。"""

    def __init__(self, base_url: str | None = None, timeout: float = 30.0):
        self._base_url = base_url or BASE_URL
        self._timeout = timeout
        self._api_key: str | None = None

    def set_api_key(self, api_key: str) -> None:
        """设置 API Key 用于鉴权。"""
        self._api_key = api_key

    async def search(self, params: ImporterCycleQueryParams) -> ImporterCycleQueryResult:
        """执行采购商贸易趋势查询。"""
        return await self._search_api(params)

    async def _search_api(self, params: ImporterCycleQueryParams) -> ImporterCycleQueryResult:
        body = params.to_api_body()
        print("==================importer_cycle_analysis body")
        print(body)

        headers: dict[str, str] = {}
        headers["Content-Type"] = "application/json"
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        url = BASE_URL + "/importer_cycle_analysis"

        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(body)
        )

        data = response.json().get("data", {})
        if (response.json().get("code")!=200):
            return ImporterCycleQueryResult(               
                code=response.json().get("code"),
                message=response.json().get("message", ""),
            )
        
        items = data.get("result", [])

        total = data.get("total", len(items))
        page_size = int(data.get("pageSize", params.page_size))
        page_index = int(data.get("pageIndex", params.page_index))
        total_pages = max(1, (total + page_size - 1) // page_size)

        result = ImporterCycleQueryResult(
            records=items,
            total=total,
            page_index=page_index,
            page_size=page_size,
            total_pages=total_pages,
            query_params=params,
        )
        return result
