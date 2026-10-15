# 全球海关贸易数据 MCP

<a href="https://tradee.topease.net/" target="_blank">
  <img src="https://img.shields.io/badge/官网-tradee.topease.net-blue" alt="官网">
</a>
<a href="https://pypi.org/project/topease-mcp/" target="_blank">
  <img src="https://img.shields.io/pypi/v/topease-mcp" alt="PyPI">
</a>
<a href="https://pypi.org/project/topease-mcp/" target="_blank">
  <img src="https://img.shields.io/pypi/pyversions/topease-mcp" alt="Python">
</a>

全球海关贸易数据 MCP 服务 — 覆盖 238 个国家/地区，一站式查询进出口贸易明细与采购商、供应商企业画像分析。

## 简介

`全球海关贸易数据 MCP` 是一个 MCP（Model Context Protocol）服务器，对接 [tradee.topease.net](https://tradee.topease.net/) 海关智能体贸易数据平台。内置 **15 个工具**：海关贸易明细查询、采购商（Importer）/供应商（Exporter）企业搜索，以及围绕两大主体的关键字、贸易角色、HS 编码、贸易港口、贸易趋势、交易对手等多维度分析能力，帮助大模型快速获取真实的全球贸易情报数据。

> 使用前需在 <https://tradee.topease.net/> 注册并获取 API Key。

## 特性

- 🌍 **全球覆盖**：支持 238 个国家/地区的贸易数据查询
- 🔍 **多维度查询**：企业名称、产品关键字、HS 编码、贸易时间、进出口类型、国家联合筛选
- 🔐 **安全认证**：支持 API Key 认证，保护数据访问安全
- 🚀 **两种传输模式**：支持 stdio（桌面客户端）和 streamable-http（Web 应用）两种运行模式
- 📊 **丰富的返回字段**：包含企业信息、产品详情、贸易金额、数量、重量等完整数据
- 🧭 **双主体多维分析**：围绕采购商（importer）与供应商（exporter）各提供 7 个分析工具，覆盖关键字、贸易角色、HS 编码、港口、趋势、交易对手等维度

## 安装

### 使用 pip

```bash
pip install topease-mcp
```

### 使用 uv

```bash
uv add topease-mcp
```

### 使用 uvx（免安装，直接运行）

```bash
uvx topease-mcp
```

### 从源码安装

```bash
git clone https://github.com/topease020/topease-customs-mcp-server.git
cd topease-customs-mcp-server
uv pip install -e .
```

## 快速开始

### 方式一：stdio 模式（推荐用于 Claude Desktop、Trae 等桌面客户端）

在 Claude Desktop、Trae 等 MCP 客户端的配置文件中添加：

```json
{
  "mcpServers": {
    "topease-customs-data": {
      "command": "uvx",
      "args": ["topease-mcp"],
      "env": {
        "TOPEASE_MCP_API_KEY": "<YOUR_API_KEY>"
      }
    }
  }
}
```

或使用 pip 安装的版本：

```json
{
  "mcpServers": {
    "topease-customs-data": {
      "command": "python",
      "args": ["-m", "topease-mcp"],
      "env": {
        "TOPEASE_MCP_API_KEY": "<YOUR_API_KEY>"
      }
    }
  }
}
```

### 方式二：streamable-http 模式（推荐用于 Web 应用）

#### 公共服务地址

我们提供了公共的 streamable-http 服务，您可以直接使用以下配置：

| 配置项        | 值                                     |
| ---------- | ------------------------------------- |
| **服务类型**   | 可流式传输的 HTTP (streamableHttp)          |
| **服务 URL** | `https://mcp.topease.net/mcp`         |
| **请求头**    | `Authorization=Bearer <your_api_key>` |

#### 在大模型客户端中配置

在 Claude Desktop、Trae 等支持 streamable-http 的客户端中添加配置：

```json
{
  "mcpServers": {
    "【PRO】TOPEASE 贸易数据查询 stream http": {
      "type": "streamableHttp",
      "url": "https://mcp.topease.net/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_API_KEY>"
      }
    }
  }
}
```

## API Key 配置说明

本服务支持两种 API Key 配置方式（按优先级排序）：

1. **环境变量**（推荐）：设置 `TOPEASE_MCP_API_KEY` 环境变量
2. **HTTP 请求头**（streamable-http 模式）：通过 `Authorization: Bearer <your_api_key>` 请求头传递

## 可用工具

当前共注册 **15 个工具**：

| 分类       | 工具                           | 说明              |
| -------- | ---------------------------- | --------------- |
| 海关贸易数据查询 | `search_customs_data`        | 海关贸易明细查询        |
| 采购商搜索    | `search_importer_data`       | 采购商（进口商）企业搜索    |
| 采购商分析    | `importer_keyword_analysis`  | 贸易关键字统计         |
| 采购商分析    | `importer_role_analysis`     | 贸易角色分布          |
| 采购商分析    | `importer_hscode_analysis`   | 贸易编码（HS Code）统计 |
| 采购商分析    | `importer_port_analysis`     | 贸易港口统计          |
| 采购商分析    | `importer_cycle_analysis`    | 贸易趋势（按月统计）      |
| 采购商分析    | `importer_exporter_analysis` | 贸易供应商（上游）列表     |
| 供应商搜索    | `search_exporter_data`       | 供应商（出口商）企业搜索    |
| 供应商分析    | `exporter_keyword_analysis`  | 贸易关键字统计         |
| 供应商分析    | `exporter_role_analysis`     | 贸易角色分布          |
| 供应商分析    | `exporter_hscode_analysis`   | 贸易编码（HS Code）统计 |
| 供应商分析    | `exporter_port_analysis`     | 贸易港口统计          |
| 供应商分析    | `exporter_cycle_analysis`    | 贸易趋势（按月统计）      |
| 供应商分析    | `exporter_importer_analysis` | 贸易采购商（客户）列表     |

### search\_customs\_data

查询海关贸易数据。支持多维度联合过滤。

| 参数                | 类型     | 必填 | 说明                                          | 默认值         |
| ----------------- | ------ | -- | ------------------------------------------- | ----------- |
| `company_name`    | string | 否  | 企业名称（模糊匹配进口商/出口商）                           | -           |
| `product_keyword` | string | 否  | 产品描述关键字，如 "led"、"valve"                     | -           |
| `hs_code`         | string | 否  | HS 海关编码（前缀匹配），如 "8415"                      | -           |
| `trade_type`      | string | 否  | 贸易类型：`import`（进口）、`export`（出口）、`all`（全部）    | `all`       |
| `country`         | string | 否  | 国家/地区名称（中文/英文/ISO编码均可），如 "China"、"美国"、"JP"  | -           |
| `date_from`       | string | 否  | 起始日期，格式 YYYY-MM-DD                          | -           |
| `date_to`         | string | 否  | 结束日期，格式 YYYY-MM-DD                          | -           |
| `page_index`      | int    | 否  | 页码                                          | `1`         |
| `page_size`       | int    | 否  | 每页记录数（最大 20）                                | `20`        |
| `sort_by`         | string | 否  | 排序字段：`tradedate`、`quantity`、`weight`、`uusd` | `tradedate` |
| `sort_order`      | string | 否  | 排序方向：`asc` / `desc`                         | `desc`      |

> **注意**：
>
> 1. `company_name`、`product_keyword`、`hs_code`、`country` 至少填写一个
> 2. `page_size` 最大值为 20，超出会自动截断
> 3. `trade_type` 映射：`import`→1, `export`→0, `all`→2
>
> <br />

## 返回字段说明

每条记录包含以下字段（中文键名，便于大模型理解）：

| 字段        | 说明                |
| :-------- | :---------------- |
| `单据ID`    | 单据编号              |
| `海关编码`    | HS 海关编码           |
| `产品描述`    | 产品描述              |
| `贸易类型`    | 贸易类型（`进口` / `出口`） |
| `进口商`     | 进口商名称             |
| `出口商`     | 出口商名称             |
| `数量`      | 数量                |
| `数量单位`    | 数量单位              |
| `重量`      | 重量                |
| `金额(USD)` | 金额（USD），保留 4 位小数  |
| `贸易日期`    | 贸易日期              |
| `原产国`     | 原产国               |
| `原产国ID`   | 原产国 ID            |

同时包含分页信息：

| 字段            | 说明    |
| :------------ | :---- |
| `total`       | 总记录数  |
| `page_index`  | 当前页码  |
| `page_size`   | 每页记录数 |
| `total_pages` | 总页数   |

<br />

### search\_importer\_data

查询海关数据中的**采购商（进口商）企业**。支持按产品关键字、HS 编码、企业名称、国家等多维度检索，返回采购商 TCode，可作为后续各 `importer_*` 分析工具的入参。

| 参数             | 类型     | 必填 | 说明                                               | 默认值        |
| -------------- | ------ | -- | ------------------------------------------------ | ---------- |
| `prodesc`      | string | 否  | 产品描述关键字，如 "led"                                  | -          |
| `hs_code`      | string | 否  | HS 海关编码                                          | -          |
| `company_name` | string | 否  | 采购商企业名称关键字                                       | -          |
| `country`      | string | 否  | 企业所在国家（中文名/英文名/ISO 编码均可）                         | -          |
| `from_country` | string | 否  | 采购来源国，如 "China" 表示筛选从中国采购过的采购商                   | -          |
| `recent_years` | string | 否  | 查询近几年的交易数据，范围 1-5                                | `"1"`      |
| `page_index`   | string | 否  | 页码                                               | `"1"`      |
| `page_size`    | string | 否  | 每页记录数                                            | `"10"`     |
| `sort_field`   | string | 否  | 排序字段：`amount`、`count`、`quantity`、`weight`、`teus` | `"amount"` |
| `sort_type`    | string | 否  | 排序方向：`desc` / `asc`                              | `"desc"`   |

> **注意**：`prodesc`、`hs_code`、`company_name` 至少填写一项。

**返回字段（records 列表每个元素）：**

| 字段               | 类型         | 说明                       |
| ---------------- | ---------- | ------------------------ |
| `TCode`          | Encryption | 采购商 TCode（唯一标识，用于后续分析工具） |
| `name`           | String     | 企业名称                     |
| `countryId`      | Long       | 企业所在国家 ID                |
| `relatedCount`   | Long       | 相关交易单数                   |
| `totalCount`     | Long       | 总交易单数                    |
| `maxTradeDate`   | String     | 企业最近贸易时间                 |
| `relatedHsCode`  | String     | 关联产品编码                   |
| `relatedProduct` | String     | 关联产品描述                   |

附加注入字段：`countryCnName` / `countryName`（企业所在国家中英文名）、`fromCountryCnName` / `fromCountryName`（采购来源国中英文名）。

### search\_exporter\_data

查询海关数据中的**供应商（出口商）企业**。参数结构与 `search_importer_data` 一致，差异点：`to_country` 为销售目的国。

| 参数             | 类型     | 必填 | 说明                                               | 默认值        |
| -------------- | ------ | -- | ------------------------------------------------ | ---------- |
| `prodesc`      | string | 否  | 产品描述关键字，如 "led"                                  | -          |
| `hs_code`      | string | 否  | HS 海关编码                                          | -          |
| `company_name` | string | 否  | 供应商企业名称关键字                                       | -          |
| `country`      | string | 否  | 企业所在国家（中文名/英文名/ISO 编码均可）                         | -          |
| `to_country`   | string | 否  | 销售目的国，如 "United States" 表示筛选销售到美国的供应商            | -          |
| `recent_years` | string | 否  | 查询近几年的交易数据，范围 1-5                                | `"1"`      |
| `page_index`   | string | 否  | 页码                                               | `"1"`      |
| `page_size`    | string | 否  | 每页记录数                                            | `"10"`     |
| `sort_field`   | string | 否  | 排序字段：`amount`、`count`、`quantity`、`weight`、`teus` | `"amount"` |
| `sort_type`    | string | 否  | 排序方向：`desc` / `asc`                              | `"desc"`   |

**返回字段（records 列表每个元素）：** 与 `search_importer_data` 相同（`TCode` 为供应商 TCode）；附加注入字段为 `countryCnName` / `countryName`、`toCountryCnName` / `toCountryName`（销售目的国中英文名）。

### importer\_cycle\_analysis

查询指定**采购商**的贸易趋势（按月统计）。传入采购商 TCode，按月返回贸易次数、金额、数量、重量、箱量，可用于观察采购商的贸易季节性和周期性变化。

| 参数           | 类型     | 必填    | 说明                                                    | 默认值           |
| ------------ | ------ | ----- | ----------------------------------------------------- | ------------- |
| `t_code`     | string | **是** | 采购商 ID（TCode）。可先通过 `search_importer_data` 工具查询采购商获取   | -             |
| `hs_code`    | string | 否     | HS 海关编码前缀过滤                                           | -             |
| `prodesc`    | string | 否     | 提单描述关键字，进一步过滤结果                                       | -             |
| `b_date`     | string | 否     | 交易起始日期，格式 `yyyy-MM-dd`                                | -             |
| `e_date`     | string | 否     | 交易结束日期，格式 `yyyy-MM-dd`                                | -             |
| `page_index` | string | 否     | 页码                                                    | `"1"`         |
| `page_size`  | string | 否     | 每页记录数，默认 `"12"`（对应 12 个月）                             | `"12"`        |
| `sort_field` | string | 否     | 排序字段：`tradeDate`、`quantity`、`weight`、`amount`、`count` | `"tradeDate"` |
| `sort_type`  | string | 否     | 排序方向：`desc` / `asc`                                   | `"desc"`      |

**返回字段（records 列表每个元素）：**

| 字段          | 类型      | 说明                 |
| ----------- | ------- | ------------------ |
| `tradeDate` | String  | 交易月份，如 `"2025-01"` |
| `teus`      | Decimal | 贸易总箱量（TEU）         |
| `count`     | Long    | 贸易次数               |
| `amount`    | Decimal | 贸易总金额              |
| `quantity`  | Decimal | 贸易总数量              |
| `weight`    | Decimal | 贸易总重量              |

同时包含分页字段：`total`、`pageSize`、`pageIndex`。

### importer\_keyword\_analysis

查询指定**采购商**的企业关联产品关键字统计，了解该采购商主要采购哪些产品。

| 参数           | 类型     | 必填    | 说明                                          | 默认值    |
| ------------ | ------ | ----- | ------------------------------------------- | ------ |
| `t_code`     | string | **是** | 采购商 ID（TCode），可通过 `search_importer_data` 获取 | -      |
| `page_index` | string | 否     | 页码                                          | `"1"`  |
| `page_size`  | string | 否     | 每页记录数                                       | `"10"` |

**返回字段（records 列表每个元素）：**

| 字段             | 类型      | 说明     |
| -------------- | ------- | ------ |
| `keyword`      | String  | 关键字    |
| `count`        | Long    | 贸易次数   |
| `countPercent` | Decimal | 贸易次数占比 |

### importer\_role\_analysis

查询指定**采购商**的贸易角色分布（采购商/供应商）及数据源国家、数据源类型。

| 参数           | 类型     | 必填    | 说明                                        | 默认值        |
| ------------ | ------ | ----- | ----------------------------------------- | ---------- |
| `t_code`     | string | **是** | 采购商 ID（TCode）                             | -          |
| `sort_field` | string | 否     | 排序字段：`quantity`、`weight`、`amount`、`count` | `"amount"` |
| `sort_type`  | string | 否     | 排序方向：`desc` / `asc`                       | `"desc"`   |

**返回字段（records 列表每个元素）：**

| 字段                  | 类型      | 说明               |
| ------------------- | ------- | ---------------- |
| `role`              | String  | 贸易角色（采购商/供应商）    |
| `dataSourceCountry` | String  | 数据源国家，如 "美国,加拿大" |
| `dataSourceType`    | String  | 数据源类型（进口/出口）     |
| `amount`            | Decimal | 贸易总金额            |
| `count`             | Long    | 贸易总次数            |
| `amountPercent`     | Decimal | 贸易金额占比           |
| `countPercent`      | Decimal | 贸易次数占比           |

### importer\_hscode\_analysis

查询指定**采购商**的 HS 编码维度贸易统计，含各维度占比及中英文海关编码描述。

| 参数           | 类型     | 必填    | 说明                                               | 默认值        |
| ------------ | ------ | ----- | ------------------------------------------------ | ---------- |
| `t_code`     | string | **是** | 采购商 ID（TCode）                                    | -          |
| `prodesc`    | string | 否     | 提单描述关键字                                          | -          |
| `hs_code`    | string | 否     | HS 编码                                            | -          |
| `b_date`     | string | 否     | 交易起始日期，格式 `yyyy-MM-dd`                           | -          |
| `e_date`     | string | 否     | 交易结束日期，格式 `yyyy-MM-dd`                           | -          |
| `page_index` | string | 否     | 页码                                               | `"1"`      |
| `page_size`  | string | 否     | 每页记录数                                            | `"10"`     |
| `sort_field` | string | 否     | 排序字段：`quantity`、`weight`、`amount`、`count`、`teus` | `"amount"` |
| `sort_type`  | string | 否     | 排序方向：`desc` / `asc`                              | `"desc"`   |

**返回字段（records 列表每个元素）：**

| 字段                                                                                     | 类型      | 说明               |
| -------------------------------------------------------------------------------------- | ------- | ---------------- |
| `hsCode`                                                                               | String  | HS 编码            |
| `count`                                                                                | Long    | 贸易次数             |
| `amount`                                                                               | Decimal | 贸易总金额            |
| `teus`                                                                                 | Decimal | 贸易总箱量            |
| `weight`                                                                               | Decimal | 贸易总重量            |
| `quantity`                                                                             | Decimal | 贸易总数量            |
| `amountPercent` / `countPercent` / `quantityPercent` / `weightPercent` / `teusPercent` | Decimal | 金额/次数/数量/重量/箱量占比 |
| `cnDescription`                                                                        | String  | 中文海关编码描述         |
| `enDescription`                                                                        | String  | 英文海关编码描述         |

### importer\_port\_analysis

查询指定**采购商**的港口维度贸易统计（起运港/卸货港）。

| 参数           | 类型     | 必填    | 说明                                               | 默认值        |
| ------------ | ------ | ----- | ------------------------------------------------ | ---------- |
| `t_code`     | string | **是** | 采购商 ID（TCode）                                    | -          |
| `prodesc`    | string | 否     | 提单描述关键字                                          | -          |
| `hs_code`    | string | 否     | HS 编码                                            | -          |
| `b_date`     | string | 否     | 交易起始日期，格式 `yyyy-MM-dd`                           | -          |
| `e_date`     | string | 否     | 交易结束日期，格式 `yyyy-MM-dd`                           | -          |
| `page_index` | string | 否     | 页码                                               | `"1"`      |
| `page_size`  | string | 否     | 每页记录数，最大 `"10"`，超出自动截断                           | `"10"`     |
| `port_type`  | string | 否     | 港口类型：`1` 起运港口，`2` 卸货港口                           | `"2"`      |
| `sort_field` | string | 否     | 排序字段：`quantity`、`weight`、`amount`、`count`、`teus` | `"amount"` |
| `sort_type`  | string | 否     | 排序方向：`desc` / `asc`                              | `"desc"`   |

**返回字段（records 列表每个元素）：**

| 字段                                                                                     | 类型      | 说明               |
| -------------------------------------------------------------------------------------- | ------- | ---------------- |
| `port`                                                                                 | String  | 港口名称             |
| `count`                                                                                | Long    | 贸易次数             |
| `amount`                                                                               | Decimal | 贸易总金额            |
| `weight`                                                                               | Decimal | 贸易总重量            |
| `quantity`                                                                             | Decimal | 贸易总数量            |
| `teus`                                                                                 | Decimal | 贸易总箱量            |
| `amountPercent` / `quantityPercent` / `countPercent` / `teusPercent` / `weightPercent` | Decimal | 金额/数量/次数/箱量/重量占比 |

### importer\_exporter\_analysis

查询指定**采购商**的贸易供应商（上游）列表，了解该采购商从哪些供应商采购、各占多少份额。

| 参数           | 类型     | 必填    | 说明                                               | 默认值        |
| ------------ | ------ | ----- | ------------------------------------------------ | ---------- |
| `t_code`     | string | **是** | 采购商 ID（TCode）                                    | -          |
| `prodesc`    | string | 否     | 提单描述关键字                                          | -          |
| `hs_code`    | string | 否     | HS 编码                                            | -          |
| `b_date`     | string | 否     | 交易起始日期，格式 `yyyy-MM-dd`                           | -          |
| `e_date`     | string | 否     | 交易结束日期，格式 `yyyy-MM-dd`                           | -          |
| `page_index` | string | 否     | 页码                                               | `"1"`      |
| `page_size`  | string | 否     | 每页记录数                                            | `"10"`     |
| `sort_field` | string | 否     | 排序字段：`quantity`、`weight`、`amount`、`count`、`teus` | `"amount"` |
| `sort_type`  | string | 否     | 排序方向：`desc` / `asc`                              | `"desc"`   |

**返回字段（records 列表每个元素）：**

| 字段                                                                                     | 类型      | 说明                |
| -------------------------------------------------------------------------------------- | ------- | ----------------- |
| `TCode`                                                                                | String  | 供应商 Tcode         |
| `supplierName`                                                                         | String  | 供应商名称             |
| `countryId`                                                                            | Long    | 企业所在国家 ID         |
| `teus` / `weight` / `quantity`                                                         | Decimal | 贸易总箱量 / 总重量 / 总数量 |
| `count`                                                                                | Long    | 贸易次数              |
| `amount`                                                                               | Decimal | 贸易总金额             |
| `amountPercent` / `countPercent` / `quantityPercent` / `weightPercent` / `teusPercent` | Decimal | 金额/次数/数量/重量/箱量占比  |

### exporter\_cycle\_analysis

查询指定**供应商**的贸易趋势（按月统计）。传入供应商 TCode，按月返回贸易次数、金额、数量、重量、箱量，可用于观察供应商的贸易季节性和周期性变化。

| 参数           | 类型     | 必填    | 说明                                                    | 默认值           |
| ------------ | ------ | ----- | ----------------------------------------------------- | ------------- |
| `t_code`     | string | **是** | 供应商 ID（TCode）。可先通过 `search_exporter_data` 工具查询供应商获取   | -             |
| `hs_code`    | string | 否     | HS 海关编码前缀过滤                                           | -             |
| `prodesc`    | string | 否     | 提单描述关键字，进一步过滤结果                                       | -             |
| `b_date`     | string | 否     | 交易起始日期，格式 `yyyy-MM-dd`                                | -             |
| `e_date`     | string | 否     | 交易结束日期，格式 `yyyy-MM-dd`                                | -             |
| `page_index` | string | 否     | 页码                                                    | `"1"`         |
| `page_size`  | string | 否     | 每页记录数，默认 `"12"`（对应 12 个月）                             | `"12"`        |
| `sort_field` | string | 否     | 排序字段：`tradeDate`、`quantity`、`weight`、`amount`、`count` | `"tradeDate"` |
| `sort_type`  | string | 否     | 排序方向：`desc` / `asc`                                   | `"desc"`      |

**返回字段（records 列表每个元素）：**

| 字段          | 类型      | 说明                 |
| ----------- | ------- | ------------------ |
| `tradeDate` | String  | 交易月份，如 `"2025-01"` |
| `teus`      | Decimal | 贸易总箱量（TEU）         |
| `count`     | Long    | 贸易次数               |
| `amount`    | Decimal | 贸易总金额              |
| `quantity`  | Decimal | 贸易总数量              |
| `weight`    | Decimal | 贸易总重量              |

同时包含分页字段：`total`、`pageSize`、`pageIndex`。

### exporter\_keyword\_analysis

查询指定**供应商**的企业关联产品关键字统计，了解该供应商主要供应哪些产品。

| 参数           | 类型     | 必填    | 说明                                          | 默认值    |
| ------------ | ------ | ----- | ------------------------------------------- | ------ |
| `t_code`     | string | **是** | 供应商 ID（TCode），可通过 `search_exporter_data` 获取 | -      |
| `page_index` | string | 否     | 页码                                          | `"1"`  |
| `page_size`  | string | 否     | 每页记录数                                       | `"10"` |

**返回字段（records 列表每个元素）：**

| 字段             | 类型      | 说明     |
| -------------- | ------- | ------ |
| `keyword`      | String  | 关键字    |
| `count`        | Long    | 贸易次数   |
| `countPercent` | Decimal | 贸易次数占比 |

### exporter\_role\_analysis

查询指定**供应商**的贸易角色分布及数据源国家、数据源类型。

| 参数           | 类型     | 必填    | 说明                                        | 默认值        |
| ------------ | ------ | ----- | ----------------------------------------- | ---------- |
| `t_code`     | string | **是** | 供应商 ID（TCode）                             | -          |
| `sort_field` | string | 否     | 排序字段：`quantity`、`weight`、`amount`、`count` | `"amount"` |
| `sort_type`  | string | 否     | 排序方向：`desc` / `asc`                       | `"desc"`   |

**返回字段（records 列表每个元素）：**

| 字段                  | 类型      | 说明           |
| ------------------- | ------- | ------------ |
| `role`              | String  | 企业角色         |
| `dataSourceCountry` | String  | 数据源国家        |
| `dataSourceType`    | String  | 数据源类型（进口/出口） |
| `count`             | Long    | 贸易次数         |
| `amount`            | Decimal | 贸易总金额        |
| `amountPercent`     | Decimal | 贸易金额占比       |
| `countPercent`      | Decimal | 贸易次数占比       |

### exporter\_hscode\_analysis

查询指定**供应商**的 HS 编码维度贸易统计，含各维度占比及中英文海关编码描述。

| 参数           | 类型     | 必填    | 说明                                               | 默认值        |
| ------------ | ------ | ----- | ------------------------------------------------ | ---------- |
| `t_code`     | string | **是** | 供应商 ID（TCode）                                    | -          |
| `prodesc`    | string | 否     | 提单描述关键字                                          | -          |
| `hs_code`    | string | 否     | HS 编码                                            | -          |
| `b_date`     | string | 否     | 交易起始日期，格式 `yyyy-MM-dd`                           | -          |
| `e_date`     | string | 否     | 交易结束日期，格式 `yyyy-MM-dd`                           | -          |
| `page_index` | string | 否     | 页码                                               | `"1"`      |
| `page_size`  | string | 否     | 每页记录数                                            | `"10"`     |
| `sort_field` | string | 否     | 排序字段：`quantity`、`weight`、`amount`、`count`、`teus` | `"amount"` |
| `sort_type`  | string | 否     | 排序方向：`desc` / `asc`                              | `"desc"`   |

**返回字段（records 列表每个元素）：** 与 `importer_hscode_analysis` 相同（`hsCode`、`count`、`amount`、`teus`、`weight`、`quantity`、各维度 `*Percent`、`cnDescription`、`enDescription`）。

### exporter\_port\_analysis

查询指定**供应商**的港口维度贸易统计。与 `importer_port_analysis` 参数一致，差异点：`port_type` 默认为 `"1"`（起运港口，供应商视角）。

| 参数           | 类型     | 必填    | 说明                                               | 默认值        |
| ------------ | ------ | ----- | ------------------------------------------------ | ---------- |
| `t_code`     | string | **是** | 供应商 ID（TCode）                                    | -          |
| `prodesc`    | string | 否     | 提单描述关键字                                          | -          |
| `hs_code`    | string | 否     | HS 编码                                            | -          |
| `b_date`     | string | 否     | 交易起始日期，格式 `yyyy-MM-dd`                           | -          |
| `e_date`     | string | 否     | 交易结束日期，格式 `yyyy-MM-dd`                           | -          |
| `page_index` | string | 否     | 页码                                               | `"1"`      |
| `page_size`  | string | 否     | 每页记录数，最大 `"10"`，超出自动截断                           | `"10"`     |
| `port_type`  | string | 否     | 港口类型：`1` 起运港口，`2` 卸货港口                           | `"1"`      |
| `sort_field` | string | 否     | 排序字段：`quantity`、`weight`、`amount`、`count`、`teus` | `"amount"` |
| `sort_type`  | string | 否     | 排序方向：`desc` / `asc`                              | `"desc"`   |

**返回字段（records 列表每个元素）：** 与 `importer_port_analysis` 相同（`port`、`count`、`amount`、`weight`、`quantity`、`teus`、各维度 `*Percent`）。

### exporter\_importer\_analysis

查询指定**供应商**的贸易采购商（客户）列表，了解该供应商把货卖给哪些采购商、各占多少份额。

| 参数           | 类型     | 必填    | 说明                                               | 默认值        |
| ------------ | ------ | ----- | ------------------------------------------------ | ---------- |
| `t_code`     | string | **是** | 供应商 ID（TCode）                                    | -          |
| `prodesc`    | string | 否     | 提单描述关键字                                          | -          |
| `hs_code`    | string | 否     | HS 编码                                            | -          |
| `b_date`     | string | 否     | 交易起始日期，格式 `yyyy-MM-dd`                           | -          |
| `e_date`     | string | 否     | 交易结束日期，格式 `yyyy-MM-dd`                           | -          |
| `page_index` | string | 否     | 页码                                               | `"1"`      |
| `page_size`  | string | 否     | 每页记录数                                            | `"10"`     |
| `sort_field` | string | 否     | 排序字段：`quantity`、`weight`、`amount`、`count`、`teus` | `"amount"` |
| `sort_type`  | string | 否     | 排序方向：`desc` / `asc`                              | `"desc"`   |

**返回字段（records 列表每个元素）：**

| 字段                                                                                     | 类型      | 说明                |
| -------------------------------------------------------------------------------------- | ------- | ----------------- |
| `TCode`                                                                                | String  | 采购商 Tcode         |
| `importerName`                                                                         | String  | 采购商名称             |
| `countryId`                                                                            | Long    | 企业所在国家 ID         |
| `amount`                                                                               | Decimal | 贸易总金额             |
| `teus` / `weight` / `quantity`                                                         | Decimal | 贸易总箱量 / 总重量 / 总数量 |
| `count`                                                                                | Long    | 贸易次数              |
| `amountPercent` / `countPercent` / `quantityPercent` / `weightPercent` / `teusPercent` | Decimal | 金额/次数/数量/重量/箱量占比  |

## 使用示例

### 示例 1：按产品关键字查询

```
请帮我查一下 LED 产品 2025 年从美国的进口数据，前 5 条
```

大模型将自动调用：

```json
{
  "product_keyword": "led",
  "country": "美国",
  "trade_type": "import",
  "date_from": "2025-01-01",
  "date_to": "2025-12-31",
  "page_index": 1,
  "page_size": 5
}
```

### 示例 2：按企业名称查询

```
查询 IKEA SUPPLY AG 公司 2025 年从美国的出口记录
```

```json
{
  "company_name": "IKEA SUPPLY AG",
  "country": "美国",
  "trade_type": "export",
  "date_from": "2025-01-01",
  "date_to": "2025-12-31"
}
```

### 示例 3：按国家和 HS 编码查询

```
查询日本 8415 类目下的进口贸易数据
```

```json
{
  "country": "Japan",
  "hs_code": "8415",
  "trade_type": "import"
}
```

### 示例 4：使用 HTTP 请求头传递 API Key（streamable-http 模式）

```bash
curl -X POST https://mcp.topease.net/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{
    "name": "search_customs_data",
    "parameters": {
      "product_keyword": "CABIN",
      "page_index": 1,
      "page_size": 10
    }
  }'
```

### 示例 5：采购商全维度分析工作流（多工具联动）

```
帮我分析一下美国的 LED 采购商，并给出其中最大采购商的采购趋势和供应商构成
```

大模型将依次调用：

```json
// 第 1 步：搜索采购商，获取 TCode
{ "tool": "search_importer_data", "parameters": { "prodesc": "led", "country": "美国" } }

// 第 2 步：查看采购趋势（按月）
{ "tool": "importer_cycle_analysis", "parameters": { "t_code": "<第1步返回的TCode>" } }

// 第 3 步：查看供应商构成
{ "tool": "importer_exporter_analysis", "parameters": { "t_code": "<第1步返回的TCode>" } }
```

> 供应商维度同理：先用 `search_exporter_data` 获取供应商 TCode，再调用 `exporter_*` 系列分析工具。

## 开发指南

### 项目结构

```
topease-mcp/
├── src/
│   └── topease_mcp/
│       ├── __init__.py                  # 包初始化
│       ├── __main__.py                  # 模块入口：python -m topease_mcp
│       ├── main.py                      # MCP 服务入口：FastMCP 服务器定义、共享鉴权逻辑与工具注册
│       ├── main_stdio.py                # stdio 模式独立入口
│       ├── auth.py                      # API Key 认证模块
│       ├── country.py                   # 238 个国家/地区数据（含 ISO 编码）
│       ├── setting.py                   # 配置项（API 地址、端口）
│       └── mcp_services/                # MCP 服务目录（每个服务 = Service 层 + 工具注册层）
│           ├── customs_search/              # 海关贸易明细搜索（search_customs_data）
│           ├── importer_search/             # 采购商企业搜索（search_importer_data）
│           ├── exporter_search/             # 供应商企业搜索（search_exporter_data）
│           ├── importer_keyword_analysis/   # 采购商-贸易关键字
│           ├── importer_role_analysis/      # 采购商-贸易角色
│           ├── importer_hscode_analysis/    # 采购商-贸易编码
│           ├── importer_port_analysis/      # 采购商-贸易港口
│           ├── importer_cycle_analysis/     # 采购商-贸易趋势
│           ├── importer_exporter_analysis/  # 采购商-贸易供应商
│           ├── exporter_keyword_analysis/   # 供应商-贸易关键字
│           ├── exporter_role_analysis/      # 供应商-贸易角色
│           ├── exporter_hscode_analysis/    # 供应商-贸易编码
│           ├── exporter_port_analysis/      # 供应商-贸易港口
│           ├── exporter_cycle_analysis/     # 供应商-贸易趋势
│           └── exporter_importer_analysis/  # 供应商-贸易采购商
├── pyproject.toml                       # 项目配置与依赖
├── README.md                            # 项目文档
└── .env.example                         # 环境变量示例
```

> 每个服务目录包含固定三个文件：`__init__.py`、`<ServiceName>Services.py`（Service 层：参数/结果数据模型 + API 请求封装）、`<tool_name>.py`（工具注册层：注册 MCP 工具并处理鉴权与参数校验）。

### 核心模块说明

- **`main.py`**：定义 FastMCP 服务器与共享鉴权逻辑（`TOPEASE_MCP_API_KEY`、`_get_api_key_from_headers`、`_format_error`），各工具注册文件由此导入
- **`mcp_services/`**：15 个 MCP 工具的实现目录，Service 层封装 API 请求、响应数据模型与字段注释，工具注册层负责参数校验与错误提示
- **`country.py`**：包含 238 个国家/地区数据，支持通过中文名、英文名、ISO 编码查找国家 ID
- **`auth.py`**：API Key 验证模块，支持环境变量配置有效密钥列表
- **`setting.py`**：集中管理 API 基础地址和端口配置

### 本地开发

```bash
# 1. 克隆项目
git clone https://github.com/topease020/topease-customs-mcp-server.git
cd topease-customs-mcp-server

# 2. 安装依赖
uv sync

# 3. 运行测试（如果有）
uv run pytest

# 4. 本地运行
uv run python -m topease_mcp
```

## 常见问题

### Q: 支持哪些国家/地区？

A: 支持全球 238 个国家和地区，包括主要贸易经济体。可通过中文名、英文名、ISO 2/3 位编码查询。

### Q: 数据更新频率是多少？

A: 数据定期更新，具体请参考 [topease.net](https://tradee.topease.net/) 官网说明。

### Q: 如何获取 API Key？

A: 访问 <https://tradee.topease.net/> 注册账号即可获取。

### Q: 查询有什么限制？

A: API 有请求频率限制，具体限制请查看 API 文档。`page_size` 最大值为 20。

### Q: 为什么工具参数中没有 `api_key`？

A: 为了简化大模型调用，API Key 通过环境变量或 HTTP 请求头配置，不再需要在每次调用时传入参数。

### Q: 如何切换 stdio 和 streamable-http 模式？

A: 修改 `main.py` 中 `mcp.run()` 的 `transport` 参数即可：

- `transport="stdio"` — 桌面客户端模式
- `transport="streamable-http"` — Web 应用模式

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

- 官网：<https://tradee.topease.net/>
- PyPI：<https://pypi.org/project/topease-mcp/>
- GitHub：<https://github.com/topease020/topease-customs-mcp-server.git>

