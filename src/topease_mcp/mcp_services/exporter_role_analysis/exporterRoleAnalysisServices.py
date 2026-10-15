"""供应商贸易角色分析模块。

根据供应商ID（TCode）查询该供应商的贸易角色统计信息，
包含贸易角色、数据源国家、数据源类型、金额/次数及其占比。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import requests
import json

from topease_mcp.setting import BASE_URL


@dataclass
class ExporterRoleQueryParams:
    """供应商贸易角色查询参数，映射到 exporter_role_analysis API。"""

    t_code: str  # 供应商ID（必填）
    sort_field: str = "amount"
    sort_type: str = "desc"

    def to_api_body(self) -> dict[str, Any]:
        """构建 API 请求体。"""
        body: dict[str, Any] = {
            "TCode": self.t_code,
            "sortField": self.sort_field,
            "sortType": self.sort_type,
        }
        return body


@dataclass
class ExporterRoleQueryResult:
    """供应商贸易角色查询结果，包含记录列表和分页信息。

    分页字段（来自 API 响应 data 对象）:
        total     (int) 符合条件的总记录数（总行数）
        page_size (int) 每页显示条数（API: data.pageSize）
        page_index (int) 当前分页索引（API: data.pageIndex）

    records 列表元素字段（每个 dict 对应接口文档"返回数据"中的 result[i]，均为必须字段）:
        role              (String)  企业角色        ← records[i]["role"]
        dataSourceCountry (String)  数据源国家      ← records[i]["dataSourceCountry"]
        dataSourceType    (String)  数据源类型      ← records[i]["dataSourceType"]
        count             (Long)    贸易次数        ← records[i]["count"]
        amount            (Decimal) 贸易总金额      ← records[i]["amount"]
        amountPercent     (Decimal) 贸易金额占比    ← records[i]["amountPercent"]
        countPercent      (Decimal) 贸易次数占比    ← records[i]["countPercent"]
    """

    # 按贸易角色统计的数据列表，每个元素为 dict，字段含义见上方 docstring
    records: list[dict[str, Any]] = field(default_factory=list)  # 元素字段: role, dataSourceCountry, dataSourceType, count, amount, amountPercent, countPercent
    total: int = 0       # 符合条件的总条数（API: data.total）
    page_index: int = 1  # 当前分页索引（API: data.pageIndex）
    page_size: int = 10  # 每页显示条数（API: data.pageSize）
    total_pages: int = 0  # 总页数 = ceil(total / page_size)
    code: int = 200
    message: str = ""
    query_params: ExporterRoleQueryParams | None = None  # 原始查询参数，用于翻页或排查

    @property
    def has_more(self) -> bool:
        return self.page_index < self.total_pages


class ExporterRoleAnalysisService:
    """供应商贸易角色分析服务，封装 exporter_role_analysis API 调用。"""

    def __init__(self, base_url: str | None = None, timeout: float = 30.0):
        self._base_url = base_url or BASE_URL
        self._timeout = timeout
        self._api_key: str | None = None

    def set_api_key(self, api_key: str) -> None:
        """设置 API Key 用于鉴权。"""
        self._api_key = api_key

    async def search(self, params: ExporterRoleQueryParams) -> ExporterRoleQueryResult:
        """执行供应商贸易角色查询。"""
        return await self._search_api(params)

    async def _search_api(self, params: ExporterRoleQueryParams) -> ExporterRoleQueryResult:
        body = params.to_api_body()
        print("==================exporter_role_analysis body")
        print(body)

        headers: dict[str, str] = {}
        headers["Content-Type"] = "application/json"
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        url = BASE_URL + "/exporter_role_analysis"

        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(body)
        )

        data = response.json().get("data", {})
        if (response.json().get("code")!=200):
            return ExporterRoleQueryResult(               
                code=response.json().get("code"),
                message=response.json().get("message", ""),
            )
        
        items = data.get("result", [])

        total = data.get("total", len(items))
        page_size = int(data.get("pageSize", len(items) or 1))
        page_index = int(data.get("pageIndex", 1))
        total_pages = max(1, (total + page_size - 1) // page_size) if page_size else 1

        result = ExporterRoleQueryResult(
            records=items,
            total=total,
            page_index=page_index,
            page_size=page_size,
            total_pages=total_pages,
            query_params=params,
        )
        return result
