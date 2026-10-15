"""供应商贸易港口分析模块。

根据供应商ID（TCode）查询该供应商的贸易港口统计信息，
包含港口名称、贸易次数/金额/数量/重量/箱量及其占比。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import requests
import json

from topease_mcp.setting import BASE_URL


@dataclass
class ExporterPortQueryParams:
    """供应商贸易港口查询参数，映射到 exporter_port_analysis API。"""

    t_code: str  # 供应商TCode（必填）
    prodesc: str | None = None
    hs_code: str | None = None
    b_date: str | None = None
    e_date: str | None = None
    page_index: str = "1"
    page_size: str = "10"
    port_type: str = "1"  # 1: 起运港口分析（默认）, 2: 卸货港口分析
    sort_field: str = "amount"
    sort_type: str = "desc"

    def to_api_body(self) -> dict[str, Any]:
        """构建 API 请求体。"""
        body: dict[str, Any] = {
            "TCode": self.t_code,
            "prodesc": self.prodesc or "",
            "hsCode": self.hs_code or "",
            "bDate": self.b_date or "",
            "eDate": self.e_date or "",
            "pageIndex": self.page_index,
            "pageSize": self.page_size,
            "portType": self.port_type,
            "sortField": self.sort_field,
            "sortType": self.sort_type,
        }
        return body


@dataclass
class ExporterPortQueryResult:
    """供应商贸易港口查询结果，包含记录列表和分页信息。

    分页字段（来自 API 响应 data 对象）:
        total     (int) 符合条件的总记录数（总行数）
        page_size (int) 每页显示条数（API: data.pageSize）
        page_index (int) 当前分页索引（API: data.pageIndex）

    records 列表元素字段（每个 dict 对应接口文档"返回数据"中的 result[i]，均为必须字段）:
        port            (String)  港口名称        ← records[i]["port"]
        count           (Long)    贸易次数        ← records[i]["count"]
        amount          (Decimal) 贸易总金额      ← records[i]["amount"]
        weight          (Decimal) 贸易总重量      ← records[i]["weight"]
        quantity        (Decimal) 贸易总数量      ← records[i]["quantity"]
        teus            (Decimal) 贸易总箱量      ← records[i]["teus"]
        amountPercent   (Decimal) 贸易金额占比    ← records[i]["amountPercent"]
        quantityPercent (Decimal) 贸易数量占比    ← records[i]["quantityPercent"]
        countPercent    (Decimal) 贸易次数占比    ← records[i]["countPercent"]
        teusPercent     (Decimal) 贸易箱量占比    ← records[i]["teusPercent"]
        weightPercent   (Decimal) 贸易重量占比    ← records[i]["weightPercent"]
    """

    # 按港口统计的贸易数据列表，每个元素为 dict，字段含义见上方 docstring
    records: list[dict[str, Any]] = field(default_factory=list)  # 元素字段: port, count, amount, weight, quantity, teus, *Percent
    total: int = 0       # 符合条件的总条数（API: data.total）
    page_index: int = 1  # 当前分页索引（API: data.pageIndex）
    page_size: int = 10  # 每页显示条数（API: data.pageSize）
    total_pages: int = 0  # 总页数 = ceil(total / page_size)
    code: int = 200
    message: str = ""
    query_params: ExporterPortQueryParams | None = None  # 原始查询参数，用于翻页或排查

    @property
    def has_more(self) -> bool:
        return self.page_index < self.total_pages


class ExporterPortAnalysisService:
    """供应商贸易港口分析服务，封装 exporter_port_analysis API 调用。"""

    def __init__(self, base_url: str | None = None, timeout: float = 30.0):
        self._base_url = base_url or BASE_URL
        self._timeout = timeout
        self._api_key: str | None = None

    def set_api_key(self, api_key: str) -> None:
        """设置 API Key 用于鉴权。"""
        self._api_key = api_key

    async def search(self, params: ExporterPortQueryParams) -> ExporterPortQueryResult:
        """执行供应商贸易港口查询。"""
        return await self._search_api(params)

    async def _search_api(self, params: ExporterPortQueryParams) -> ExporterPortQueryResult:
        body = params.to_api_body()
        print("==================exporter_port_analysis body")
        print(body)

        headers: dict[str, str] = {}
        headers["Content-Type"] = "application/json"
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        url = BASE_URL + "/exporter_port_analysis"

        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(body)
        )

        data = response.json().get("data", {})
        if (response.json().get("code")!=200):
            return ExporterPortQueryResult(               
                code=response.json().get("code"),
                message=response.json().get("message", ""),
            )
        
        items = data.get("result", [])

        total = data.get("total", len(items))
        page_size = int(data.get("pageSize", params.page_size))
        page_index = int(data.get("pageIndex", params.page_index))
        total_pages = max(1, (total + page_size - 1) // page_size)

        result = ExporterPortQueryResult(
            records=items,
            total=total,
            page_index=page_index,
            page_size=page_size,
            total_pages=total_pages,
            query_params=params,
        )
        return result
