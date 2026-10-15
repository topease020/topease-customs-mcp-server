"""供应商贸易关键字分析模块。

根据供应商ID（TCode）查询该供应商的贸易关键字统计信息，
包含关键字、贸易次数及占比。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import requests
import json

from topease_mcp.setting import BASE_URL


@dataclass
class ExporterKeywordQueryParams:
    """供应商贸易关键字查询参数，映射到 exporter_keyword_analysis API。"""

    t_code: str  # 供应商ID（必填）
    page_index: str = "1"
    page_size: str = "10"

    def to_api_body(self) -> dict[str, Any]:
        """构建 API 请求体。"""
        body: dict[str, Any] = {
            "TCode": self.t_code,
            "pageIndex": self.page_index,
            "pageSize": self.page_size,
        }
        return body


@dataclass
class ExporterKeywordQueryResult:
    """供应商贸易关键字查询结果，包含记录列表和分页信息。

    分页字段（来自 API 响应 data 对象）:
        total     (int) 符合条件的总记录数（总行数）
        page_size (int) 每页显示条数（API: data.pageSize）
        page_index (int) 当前分页索引（API: data.pageIndex）

    records 列表元素字段（每个 dict 对应接口文档"返回数据"中的 result[i]，均为必须字段）:
        keyword       (String)  关键字        ← records[i]["keyword"]
        count         (Long)    贸易次数      ← records[i]["count"]
        countPercent  (Decimal) 贸易次数占比  ← records[i]["countPercent"]
    """

    # 按关键字统计的贸易数据列表，每个元素为 dict，字段含义见上方 docstring
    records: list[dict[str, Any]] = field(default_factory=list)  # 元素字段: keyword, count, countPercent
    total: int = 0       # 符合条件的总条数（API: data.total）
    page_index: int = 1  # 当前分页索引（API: data.pageIndex）
    page_size: int = 10  # 每页显示条数（API: data.pageSize）
    total_pages: int = 0  # 总页数 = ceil(total / page_size)
    code: int = 200
    message: str = ""
    query_params: ExporterKeywordQueryParams | None = None  # 原始查询参数，用于翻页或排查

    @property
    def has_more(self) -> bool:
        return self.page_index < self.total_pages


class ExporterKeywordAnalysisService:
    """供应商贸易关键字分析服务，封装 exporter_keyword_analysis API 调用。"""

    def __init__(self, base_url: str | None = None, timeout: float = 30.0):
        self._base_url = base_url or BASE_URL
        self._timeout = timeout
        self._api_key: str | None = None

    def set_api_key(self, api_key: str) -> None:
        """设置 API Key 用于鉴权。"""
        self._api_key = api_key

    async def search(self, params: ExporterKeywordQueryParams) -> ExporterKeywordQueryResult:
        """执行供应商贸易关键字查询。"""
        return await self._search_api(params)

    async def _search_api(self, params: ExporterKeywordQueryParams) -> ExporterKeywordQueryResult:
        body = params.to_api_body()
        print("==================exporter_keyword_analysis body")
        print(body)

        headers: dict[str, str] = {}
        headers["Content-Type"] = "application/json"
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        url = BASE_URL + "/exporter_keyword_analysis"

        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(body)
        )

        data = response.json().get("data", {})
        if (response.json().get("code")!=200):
            return ExporterKeywordQueryResult(               
                code=response.json().get("code"),
                message=response.json().get("message", ""),
            )
        
        items = data.get("result", [])

        total = data.get("total", len(items))
        page_size = int(data.get("pageSize", params.page_size))
        page_index = int(data.get("pageIndex", params.page_index))
        total_pages = max(1, (total + page_size - 1) // page_size)

        result = ExporterKeywordQueryResult(
            records=items,
            total=total,
            page_index=page_index,
            page_size=page_size,
            total_pages=total_pages,
            query_params=params,
        )
        return result
