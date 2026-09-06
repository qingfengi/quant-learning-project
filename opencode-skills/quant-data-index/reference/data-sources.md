# 数据源与 API 索引

标记含义见 `../SKILL.md` §二。实测时间：2026-09-01，中国大陆网络，无代理。

---

## 1. 加密货币（币圈）

### 1.1 批量历史归档（首选，无 key 无限速）

**Binance Vision** `[OK]`
公开 S3 静态桶，按月/日打包 zip，覆盖 spot / futures 的 klines、trades、aggTrades、bookTicker、bookDepth。

```
目录浏览: https://data.binance.vision/?prefix=data/spot/daily/klines/BTCUSDT/1d/
月线包:   https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/1d/BTCUSDT-1d-2024-01.zip
日线包:   https://data.binance.vision/data/spot/daily/klines/BTCUSDT/1m/BTCUSDT-1m-2024-01-15.zip
校验:     同名 + .CHECKSUM
```

路径模板：
```
data/{spot|futures/um|futures/cm}/{monthly|daily}/{klines|trades|aggTrades|bookTicker|bookDepth|metrics|fundingRate}/{SYMBOL}/{INTERVAL}/{SYMBOL}-{INTERVAL}-{YYYY-MM[-DD]}.zip
```

klines CSV 列序（无表头）：
```
open_time, open, high, low, close, volume, close_time,
quote_volume, trades, taker_buy_base, taker_buy_quote, ignore
```

**注意**：`api.binance.com` 在大陆返回 **451** `[CN-BLOCK]`，但 `data.binance.vision` 是 CDN 静态资源，**照常可访问**。做历史回测数据集就走这条。

**CryptoDataDownload** `[OK]`
`https://www.cryptodatadownload.com/data/` — 多家交易所的 CSV 直下，覆盖已停运交易所的历史数据（Bitfinex 早期、FTX 等），做长周期研究时补缺口用。

**Tardis.dev** `[PAID]` `https://docs.tardis.dev/`
tick 级 + 完整 order book L2/L3 增量，含期权。学术免费额度需申请。做微观结构研究基本绕不开。

**Kaiko** `[PAID]` `https://docs.kaiko.com/` — 机构级 tick + 参考汇率。

### 1.2 实时/近线 REST API

| 交易所 | 端点 | 状态 |
|---|---|---|
| Binance | `https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=500` | `[CN-BLOCK]` 451 |
| Binance US | `https://api.binance.us/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=500` | `[OK]` |
| OKX | `https://www.okx.com/api/v5/market/candles?instId=BTC-USDT&bar=1D&limit=100` | `[OK]` |
| OKX 历史 | `https://www.okx.com/api/v5/market/history-candles?instId=BTC-USDT&bar=1D&after={ms}` | `[OK]` |
| Gate.io | `https://api.gateio.ws/api/v4/spot/candlesticks?currency_pair=BTC_USDT&interval=1d&limit=100` | `[OK]` |
| Huobi/HTX | `https://api.huobi.pro/market/history/kline?symbol=btcusdt&period=1day&size=200` | `[OK]` |
| Coinbase | `https://api.exchange.coinbase.com/products/BTC-USD/candles?granularity=86400` | `[OK]` |
| Kraken | `https://api.kraken.com/0/public/OHLC?pair=XBTUSD&interval=1440` | `[OK]` |
| Bitstamp | `https://www.bitstamp.net/api/v2/ohlc/btcusd/?step=86400&limit=100` | `[OK]` |
| BitMEX | `https://www.bitmex.com/api/v1/trade/bucketed?binSize=1d&symbol=XBTUSD&count=100` | `[OK]` |
| Bybit | `https://api.bybit.com/v5/market/kline?category=spot&symbol=BTCUSDT&interval=D` | `[CN-BLOCK]` 403 |

**分页要点**：OKX 用 `after`/`before` 传毫秒时间戳，单次上限 100 根，历史接口只保留有限深度；Binance 用 `startTime`/`endTime`，单次上限 1000 根。

### 1.3 衍生品 / 期权

**Deribit** `[OK]` — 加密期权的事实标准数据源，公开接口就能拉全量合约链。
```
合约列表: https://www.deribit.com/api/v2/public/get_instruments?currency=BTC&kind=option
行情:     https://www.deribit.com/api/v2/public/ticker?instrument_name=BTC-27JUN25-100000-C
K线:      https://www.deribit.com/api/v2/public/get_tradingview_chart_data?instrument_name=BTC-PERPETUAL&start_timestamp={ms}&end_timestamp={ms}&resolution=1D
```
`get_instruments` 单次返回约 850 KB，含 IV、greeks 引用字段。做隐含波动率曲面研究直接用。

资金费率历史：走 Binance Vision `futures/um/monthly/fundingRate/`，或 OKX `/api/v5/public/funding-rate-history`。

### 1.4 链上数据

| 源 | 端点 | 状态 | 内容 |
|---|---|---|---|
| Blockchair | `https://api.blockchair.com/bitcoin/stats` | `[OK]` | 多链统计、区块/交易查询，免费额度 1440 req/day |
| DefiLlama | `https://api.llama.fi/v2/chains`、`/protocols`、`/tvl/{protocol}` | `[OK]` | TVL、收益、稳定币，完全免费无 key |
| Coin Metrics Community | `https://community-api.coinmetrics.io/v4/timeseries/asset-metrics?assets=btc&metrics=PriceUSD&page_size=100` | `[OK]` | 社区版免费，含 NVT、活跃地址、实现价格等链上指标 |
| Glassnode | `https://docs.glassnode.com/` | `[OK+K]`/`[PAID]` | 链上指标标杆，免费层只放 T1 指标 |
| Santiment | `https://academy.santiment.net/sanapi/` | `[OK+K]` | GraphQL，含社交情绪指标 |
| Amberdata | `https://docs.amberdata.io/` | `[OK+K]` | 链上 + 市场 + DeFi |
| Dune Analytics | `https://docs.dune.com/` | `[OK+K]` | SQL 查询任意链上数据，免费层有 credit 限制 |
| The Graph | `https://thegraph.com/docs/en/` | `[OK]` | 去中心化子图，DEX 交易明细（Uniswap 等）走这里 |
| Messari | `https://docs.messari.io/` | `[CN-BLOCK]` | 资产基本面 |
| CryptoCompare | `https://min-api.cryptocompare.com/` | `[OK+K]` 401 无 key | 多所聚合价格 |
| CoinAPI | `https://docs.coinapi.io/` | `[CN-BLOCK]` 403 | 聚合行情 |

**CoinGecko** `[OK]`
```
健康检查: https://api.coingecko.com/api/v3/ping
币种列表: https://api.coingecko.com/api/v3/coins/list
历史日线: https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=365&interval=daily
OHLC:     https://api.coingecko.com/api/v3/coins/bitcoin/ohlc?vs_currency=usd&days=30
```
免费层 10-30 req/min，无 key。做市值排名、板块分类最方便。

### 1.5 币圈量化框架

| 项目 | 地址 | 状态 | 定位 |
|---|---|---|---|
| CCXT | `https://docs.ccxt.com/` | `[OK]` | 100+ 交易所统一 API，抓数据的第一选择 |
| Freqtrade | `https://www.freqtrade.io/en/stable/` | `[OK]` | 开箱即用的策略框架，自带数据下载 + 超参优化 |
| Hummingbot | `https://hummingbot.org/` | `[OK]` | 做市 / 套利机器人 |
| NautilusTrader | `https://nautilustrader.io/docs/latest/` | `[OK]` | Rust 内核事件驱动回测，纳秒级，支持股票+加密 |

---

## 2. A股

### 2.1 东方财富（大陆最省事，无需 Referer）

**日线 K 线** `[OK]`
```
https://push2his.eastmoney.com/api/qt/stock/kline/get
  ?secid=1.600519
  &fields1=f1,f2,f3,f4,f5
  &fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61
  &klt=101&fqt=1&beg=0&end=20500101&lmt=10000
```

secid 前缀规则：

| 前缀 | 市场 | 示例 |
|---|---|---|
| `1.` | 上交所 | `1.600519` 贵州茅台 |
| `0.` | 深交所（含创业板） | `0.000001`、`0.300750` |
| `116.` | 港股 | `116.00700` 腾讯 |
| `105.` | 纳斯达克 | `105.AAPL` |
| `106.` | 纽交所 | `106.BABA` |
| `107.` | 美交所 | — |
| `100.` | 全球指数 | `100.NDX` |
| `8.` | 北交所 | `0.` 也可试 |

`klt`：`1`=1分 `5`=5分 `15` `30` `60` `101`=日 `102`=周 `103`=月
`fqt`：`0`=不复权 `1`=前复权 `2`=后复权

`fields2` 字段序：`f51`日期 `f52`开 `f53`收 `f54`高 `f55`低 `f56`成交量 `f57`成交额 `f58`振幅 `f59`涨跌幅 `f60`涨跌额 `f61`换手率

**全市场实时快照** `[OK]`
```
https://push2.eastmoney.com/api/qt/clist/get
  ?pn=1&pz=100&po=1&fltt=2&invt=2&fid=f3
  &fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23
  &fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f14,f15,f16,f17,f18,f20,f21,f23
```
`fs` 是市场筛选串。常用组合：
- 沪深 A 股：`m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23`
- 港股主板：`m:128+t:3,m:128+t:4,m:128+t:1,m:128+t:2`
- 美股：`m:105,m:106,m:107`
- 概念板块：`m:90+t:3`
- 行业板块：`m:90+t:2`

**北向/南向资金** `[OK]`
```
https://push2.eastmoney.com/api/qt/kamt/get?fields1=f1,f2,f3,f4&fields2=f51,f52,f54,f56
```

### 2.2 新浪财经

**实时报价** `[OK+H]`（必须带 Referer）
```
https://hq.sinajs.cn/list=sh600519,sz000001,hk00700,gb_aapl
Referer: https://finance.sina.com.cn
```
返回 GBK 编码的 JS 赋值语句，用 `,` 分割。A股 33 个字段，港股 18 个，美股另一套。**注意解码用 `gbk`，直接 utf-8 会乱码。**

**港股列表分页** `[OK]`
```
https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHKStockData
  ?page=1&num=80&sort=symbol&asc=1&node=qbgg_hk
```

### 2.3 腾讯财经 `[OK]`

**复权 K 线**
```
https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sh600519,day,,,320,qfq
```
`param` = `代码,周期,起始日,结束日,数量,复权方式`。周期支持 `day/week/month/m5/m15/m30/m60`，复权 `qfq/hfq/空`。

分笔明细：`https://web.ifzq.gtimg.cn/appstock/app/dealCount/get?code=sh600519`

### 2.4 交易所官方

**上交所** `[OK+H]`
```
股票列表: http://query.sse.com.cn/security/stock/getStockListData2.do
            ?isPagination=true&stockType=1&pageHelp.pageSize=100&pageHelp.pageNo=1
            &pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=1
Referer: http://www.sse.com.cn/
公告:     http://www.sse.com.cn/disclosure/listedinfo/announcement/   [OK]
```
`stockType`：`1`=主板A `2`=主板B `8`=科创板

**深交所** `[OK+H]`
```
http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1110&TABKEY=tab1&PAGENO=1
Referer: http://www.szse.cn/market/product/stock/list/index.html
```
`CATALOGID` 是报表编号：`1110`=股票列表 `1815_stock_snapshot`=快照 `1803_sczm`=市场总貌。裸请求 **403**，必须带 Referer。

**巨潮资讯（cninfo）公告全文检索** `[OK+H]` — POST
```
POST http://www.cninfo.com.cn/new/hisAnnouncement/query
Content-Type: application/x-www-form-urlencoded
Referer: http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice
X-Requested-With: XMLHttpRequest

pageNum=1&pageSize=30&column=szse&tabName=fulltext&plate=&stock=&searchkey=
&secid=&category=&trade=&seDate=2024-01-01~2024-12-31&sortName=&sortType=&isHLtitle=true
```
`column`：`szse`=深市 `sse`=沪市 `third`=三板 `bj`=北交所
`category`：`category_ndbg_szsh`=年报 `category_bndbg_szsh`=半年报 `category_yjdbg_szsh`=一季报 `category_sjdbg_szsh`=三季报 `category_yjygjxz_szsh`=业绩预告
返回里 `adjunctUrl` 拼上 `http://static.cninfo.com.cn/` 就是 PDF 直链。**这是 A股财报 PDF 最干净的批量入口。**

裸 GET 返回 500，必须 POST + Referer。

**中证指数** `[OK]`
```
指数行情: https://www.csindex.com.cn/csindex-home/perf/index-perf?indexCode=000300&startDate=20240101&endDate=20241231
成分股:   https://csi-web-dev.oss-cn-shanghai-finance-1-pub.aliyuncs.com/static/html/csindex/public/uploads/file/autofile/cons/000300cons.txt
详情页:   https://www.csindex.com.cn/en/indices/index-detail/000300
```

**证监会** `[OK]` `http://www.csrc.gov.cn/` — 处罚决定、IPO 审核进度、政策原文。

### 2.5 宏观 / 债券

| 源 | 地址 | 状态 |
|---|---|---|
| 中债估值曲线 | `https://yield.chinabond.com.cn/` | `[OK]` |
| 人民银行 | `http://www.pbc.gov.cn/` | `[OK]` |
| 国家统计局首页 | `https://data.stats.gov.cn/` | `[OK]` |
| 统计局 easyquery API | `https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgyd&...` | `[CN-BLOCK]` 403，需完整浏览器指纹，建议改用 akshare 封装 |
| FRED（含中国宏观） | `https://fred.stlouisfed.org/`，API `https://api.stlouisfed.org/fred/series/observations?series_id=CPIAUCSL&api_key=KEY&file_type=json` | `[OK+K]` 免费 key |

### 2.6 Python 数据库封装（强烈推荐先试这层）

| 库 | 地址 | 状态 | 说明 |
|---|---|---|---|
| **AKShare** | `https://akshare.akfamily.xyz/` | `[OK]` | 免费无需注册，A股/港股/美股/期货/基金/宏观/加密全覆盖，接口 1000+。**首选**。`pip install akshare` |
| **Tushare Pro** | `https://tushare.pro/` | `[OK+K]` | 注册送积分，积分决定接口权限。数据规整度高于 akshare，适合入库 |
| **BaoStock** | `http://baostock.com/` | `[OK]` | 完全免费，A股日线/分钟线/财务，无需 token，稳定但更新略慢 |
| efinance | `https://github.com/Micro-sheep/efinance` | — | 东财接口的封装 |
| JQData | `https://www.joinquant.com/help/api/help#JQData` | `[OK+K]` | 聚宽，免费额度有限 |
| RQData | `https://www.ricequant.com/` | `[PAID]` | 米筐 |
| Wind API | `https://www.wind.com.cn/` | `[PAID]` | 机构标配，需终端授权 |
| Choice | `https://choice.eastmoney.com/` | `[PAID]` | 东财终端 |
| CSMAR/国泰安 | `https://www.gtarsc.com/` | `[PAID]` | 学术研究标配（该站 TLS 配置老旧，浏览器打开） |
| RESSET | `http://www.resset.cn/` | `[PAID]` | 学术数据库 |

**akshare 常用入口速查**：
```python
import akshare as ak
ak.stock_zh_a_hist(symbol="600519", period="daily", start_date="20200101", adjust="qfq")
ak.stock_zh_a_spot_em()                       # 全 A 实时
ak.stock_hk_hist(symbol="00700", period="daily", adjust="qfq")
ak.stock_us_hist(symbol="105.AAPL", period="daily", adjust="qfq")
ak.stock_financial_abstract(symbol="600519")  # 财务摘要
ak.stock_hsgt_north_net_flow_in_em(symbol="沪股通")
ak.macro_china_cpi()
ak.crypto_js_price()
ak.stock_lhb_detail_em(start_date="20240101", end_date="20240131")  # 龙虎榜
ak.stock_margin_detail_sse(date="20240115")   # 两融
```

---

## 3. 港股

| 用途 | 地址 | 状态 |
|---|---|---|
| HKEX 市场统计总入口 | `https://www.hkex.com.hk/Market-Data/Statistics?sc_lang=en` | `[OK]` |
| 沪深港通历史统计 | `https://www.hkex.com.hk/Mutual-Market/Stock-Connect/Statistics/Historical-Monthly?sc_lang=en` | `[OK]` |
| **CCASS 中央结算持股** | `https://www3.hkexnews.hk/sdw/search/searchsdw.aspx` | `[OK]` POST 表单 |
| 披露易（公告/年报） | `https://www1.hkexnews.hk/` | `[OK]` |
| HKEX 实时报价 widget | `https://www1.hkex.com.hk/hkexwidget/data/getequityquote?sym=700&token=...` | `[COOKIE]` 403，token 有时效，需先访问行情页抓取 |
| AASTOCKS | `http://www.aastocks.com/en/stocks/market/bmpsearch.aspx` | `[OK]` |
| 经济通 ETNet | `https://www.etnet.com.hk/www/eng/stocks/index.php` | `[OK]` |
| 东方财富港股 K线 | `push2his...?secid=116.00700&klt=101&fqt=1` | `[OK]` |
| 新浪港股 | `https://hq.sinajs.cn/list=hk00700` + Referer | `[OK+H]` |

**CCASS 抓取要点**：`searchsdw.aspx` 是 ASP.NET WebForms，POST 必须回带 `__VIEWSTATE`、`__VIEWSTATEGENERATOR`、`__EVENTVALIDATION`。流程：GET 页面 → 正则抽三个隐藏字段 → POST 带上 `txtStockCode`（5 位，如 `00700`）和 `txtShareholdingDate`。这是研判港股筹码集中度的核心数据，没有替代品。

**券商 OpenAPI（含港股实时 + 交易）**：

| 券商 | 文档 | 状态 |
|---|---|---|
| 富途 FutuOpenAPI | `https://openapi.futunn.com/futu-api-doc/en/` | `[OK+K]` 需开户 + 本地 OpenD 网关 |
| 长桥 LongPort | `https://open.longportapp.com/en/docs` | `[OK+K]` |
| 老虎 TigerOpen | `https://quant.itigerup.com/openapi/en/python/overview/prepare.html` | `[OK+K]` |
| moomoo | `https://www.moomoo.com/` | `[OK+K]` |

券商接口的优势：**同一套 API 拿港股 + 美股 + A股通，且是 L1/L2 实时**。做实盘只能走这条。

---

## 4. 美股

### 4.1 免费行情

| 源 | 端点 | 状态 |
|---|---|---|
| **Stooq**（CSV 直下，最省事） | `https://stooq.com/q/d/l/?s=aapl.us&i=d` | `[OK]` |
| Yahoo Finance chart | `https://query1.finance.yahoo.com/v8/finance/chart/AAPL?range=10y&interval=1d&events=div,split` | `[OK]` |
| 东方财富美股 | `push2his...?secid=105.AAPL&klt=101&fqt=1` | `[OK]` |
| NASDAQ screener | `https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&exchange=NASDAQ` | `[CN-BLOCK]` 超时 |

Stooq 参数：`i=d/w/m/q/y`（日周月季年），`d1=20200101&d2=20241231` 限定区间。指数用 `^spx`、`^ndq`，外汇用 `eurusd`，期货用 `cl.f`。返回标准 CSV `Date,Open,High,Low,Close,Volume`。**无 key、无限速、可直接 `pandas.read_csv(url)`。**

Yahoo chart 返回 JSON，`chart.result[0].indicators.adjclose` 是复权收盘价，`events` 里带分红拆股。注意它会偶发 429，加退避。

### 4.2 SEC EDGAR（财报数据的权威源，免费）

**必须设置 `User-Agent: 姓名 邮箱`，否则 403。这是 SEC 的硬性规定。**

```
XBRL 单指标时序:
https://data.sec.gov/api/xbrl/companyconcept/CIK0000320193/us-gaap/Assets.json   [OK+H]

公司全部财务事实:
https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json

全市场同一指标横截面:
https://data.sec.gov/api/xbrl/frames/us-gaap/Assets/USD/CY2023Q4I.json

公司申报索引:
https://data.sec.gov/submissions/CIK0000320193.json

季度全量申报索引（批量下载入口）:
https://www.sec.gov/Archives/edgar/full-index/2024/QTR1/          [OK]
  form.idx / company.idx / master.idx

CIK ↔ ticker 映射:
https://www.sec.gov/files/company_tickers.json

财务报表数据集（打包 zip，按季）:
https://www.sec.gov/dera/data/financial-statement-data-sets.html
```

要构建全市场基本面面板，标准做法是：下 `full-index` 的 `master.idx` → 筛 10-K/10-Q → 逐条取 `companyfacts.json`。或直接用 DERA 的季度 zip，省掉几万次请求。

### 4.3 商业 API（有免费层）

| 源 | 文档 | 状态 | 免费层 |
|---|---|---|---|
| Alpha Vantage | `https://www.alphavantage.co/documentation/` | `[OK+K]` | 25 req/day，含技术指标、财报、外汇、加密 |
| Finnhub | `https://finnhub.io/docs/api` | `[OK+K]` | 60 req/min，含新闻情绪、内部交易 |
| Twelve Data | `https://twelvedata.com/docs` | `[OK+K]` | 800 req/day |
| Tiingo | `https://www.tiingo.com/documentation/general/overview` | `[OK+K]` | 日线免费，含新闻 |
| Polygon.io | `https://polygon.io/docs` | `[OK+K]` | 免费层 5 req/min，付费给 tick 和期权全链 |
| Alpaca | `https://docs.alpaca.markets/` | `[OK+K]` | 免费纸交易 + IEX 数据，付费给 SIP |
| Databento | `https://databento.com/docs` | `[OK]` `[PAID]` | 按量付费，MBO 逐笔委托，做微观结构性价比高 |
| FirstRate Data | `https://firstratedata.com/` | `[PAID]` | 一次性买断分钟级历史 |
| Dukascopy | `https://www.dukascopy.com/swiss/english/marketwatch/historical/` | `[OK]` | 免费 tick 级外汇/CFD |
| IBKR API | `https://www.interactivebrokers.com/campus/category/ibkr-api-software/` | `[CN-BLOCK]` | 需开户 |

### 4.4 学术级数据库（机构授权）

| 源 | 地址 | 内容 |
|---|---|---|
| WRDS | `https://wrds-www.wharton.upenn.edu/` `[OK]` | 学术金融数据总门户，CRSP/Compustat/IBES/TAQ 都在里面 |
| CRSP | `https://www.crsp.org/` `[OK]` | 美股全历史价格 + 退市股（生存偏差修正的关键） |
| Compustat | `https://www.marketplace.spglobal.com/en/datasets/compustat-financials-(8)` `[OK]` | 标准化财务 |
| LOBSTER | `https://lobsterdata.com/` `[OK]` | NASDAQ ITCH 重构的限价订单簿，做 LOB 深度学习的标准数据集 |
| TAQ | 经 WRDS | 逐笔成交与报价 |

### 4.5 因子数据（免费，做研究的起点）

**Kenneth French Data Library** `[OK]`
`https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html`
Fama-French 3/5 因子、动量、行业组合、国际市场版本，全部 CSV/zip 直下。任何做因子研究的论文复现都从这里开始。

中国版三因子/五因子：Liu-Stambaugh-Yuan (2019) 的数据由作者提供，或从 CSMAR/Tushare 自行构造。

---

## 5. 跨市场 / 数据集平台

| 源 | 地址 | 状态 |
|---|---|---|
| Kaggle Datasets | `https://www.kaggle.com/datasets?search=cryptocurrency` | `[OK]` |
| HuggingFace Datasets | `https://huggingface.co/datasets?search=stock` | `[OK]` |
| Numerai | `https://docs.numer.ai/` | `[OK]` 匿名化特征 + 加密目标，免费 |
| QuantConnect Data | `https://www.quantconnect.com/docs/v2/writing-algorithms/datasets/overview` | `[OK]` 云端数据集市场 |
| WorldQuant BRAIN | `https://platform.worldquantbrain.com/` | `[OK+K]` 免费注册用其数据挖 alpha |
| 聚宽社区研究 | `https://www.joinquant.com/view/community/list?listType=1` | `[OK]` 中文策略与因子实证 |
| 优矿 UQER | `https://uqer.datayes.com/` | `[OK]` |
| 米筐 | `https://www.ricequant.com/` | `[OK]` |

---

## 6. 失效记录

| 日期 | 条目 | 现象 | 替代 |
|---|---|---|---|
| 2026-09-01 | `api.binance.com` | 451 大陆封锁 | `api.binance.us` / OKX / Gate；历史数据走 `data.binance.vision` |
| 2026-09-01 | `api.bybit.com` | 403 | OKX / Gate |
| 2026-09-01 | `xueqiu.com` kline | 400，需 `xq_a_token` cookie | Playwright 持久化登录，或改用东财 |
| 2026-09-01 | `data.stats.gov.cn/easyquery.htm` | 403 | `akshare` 的 macro_china_* 系列 |
| 2026-09-01 | `hkexwidget` getequityquote | 403，token 时效 | 东财 `116.` 前缀 / AASTOCKS |
| 2026-09-01 | `api.nasdaq.com/screener` | 连接超时 | Stooq / Yahoo |
| 2026-09-01 | `min-api.cryptocompare.com` | 401 无 key | 注册免费 key 或改用 CoinGecko |
| 2026-09-01 | `docs.coinapi.io`、`docs.messari.io`、SSRN、Wiley、OUP | 403 / 连接中止 | 见 papers.md 的镜像与替代检索 |
