---
name: quant-data-index
description: 需要查找加密货币（币圈）、A股、港股、美股的行情数据下载源、公开或前沿量化算法、以及相关学术论文时使用。内含 API 端点历史可用性记录、爬虫路径、批量下载地址、算法库索引和论文检索接口（arXiv/Crossref/OpenAlex），并提供五个公开来源的探活和取样工具。用户提到"币圈数据""A股数据下载""港股/美股行情 API""量化因子""alpha 算法""LOB 高频""找论文""数据源索引""爬虫入口"时触发。
---

# 币圈 / A股 / 港股 / 美股 · 数据·算法·论文 索引

这份 skill 提供数据来源索引，并附带少量真实样本的下载工具。它告诉你**去哪儿下、用什么 URL、返回什么格式、有没有坑**。

原文记录的检查日期为 2026-09-01。以下状态属于历史记录，不代表现在仍然可用，也不代表本次逐条重新验证过。鉴权和限额以服务商当前文档与实际响应为准。

---

## 一、先决定去哪张表

| 你要做什么 | 打开哪个文件 |
|---|---|
| 找行情/财务/链上数据的下载地址和 API | `reference/data-sources.md` |
| 找因子挖掘、预测模型、执行算法、开源框架 | `reference/algorithms.md` |
| 找论文、找检索接口、找必读清单 | `reference/papers.md` |
| 检查内置五个公开来源的响应是否有效 | `scripts/probe_sources.py` |
| 立刻取一段真实数据跑通链路 | `scripts/fetch_examples.py` |

---

## 二、可用性标记的含义

每条源后面都有一个标记，含义固定：

| 标记 | 含义 | 处理方式 |
|---|---|---|
| `[OK]` | 匿名直连，实测 200 | 直接用 |
| `[OK+H]` | 必须补 `Referer` 或 `User-Agent` 才通 | 照抄该条给的请求头 |
| `[OK+K]` | 需要免费注册拿 key | 先注册，key 放环境变量 |
| `[CN-BLOCK]` | 大陆网络被拦（451/403/超时） | 换镜像域名或走代理 |
| `[COOKIE]` | 需要登录态 cookie | 用 Playwright 持久化 profile |
| `[PAID]` | 商业授权 | 记路径，别硬爬 |

---

## 三、三条硬规则

### 规则一：先探活，再写抓取代码

网站结构和风控每季度都在变。动手前先跑：

```powershell
python .opencode\skills\quant-data-index\scripts\probe_sources.py --group crypto
python .opencode\skills\quant-data-index\scripts\probe_sources.py --all
```

输出会直接告诉你哪条挂了。**不要在明知失效的端点上反复调参数。**

需要 Python 3.10+，仅使用标准库。命令中的 `.opencode/skills/quant-data-index/` 是安装路径；若在独立仓库或此 Skill 目录运行，将前缀替换为 `scripts/`。

```powershell
python scripts/probe_sources.py --list
python scripts/probe_sources.py --source gate-futures --timeout 10
python scripts/fetch_examples.py --source gate-futures --limit 5 --output output/gate-futures.json
python scripts/fetch_examples.py --source crossref --query "quantitative trading" --output output/papers.json
python -m unittest discover -s tests -v
```

内置来源：`gate-spot`、`gate-futures`、`binance` 属于 `crypto` 组；`arxiv`、`crossref` 属于 `papers` 组。`--all` 仅检查这五个样本接口，参考文档中的其他接口仍需单独核对。不会自动更换交易所，也不会读取本地凭据。

探活验证 HTTP 状态、JSON/Atom 结构、必要字段和非空样本。全部成功退出 0，某来源失败退出 1，参数错误退出 2。取样要求明确的 `--source` 和 `--output`，每次最多 100 条，响应体不超过 2 MiB；已有输出文件不会被覆盖，网络或格式失败不会伪造数据。支持正常的零条论文搜索结果。超时默认 15 秒，可设为大于 0、不超过 60 秒，是每次网络操作的等待上限；没有自动重试。

输出记录公开请求 URL、获取时间和数据。价格以文本保存以保留小数精度；Gate 现货成交量单位为 USDT，Gate 永续合约为合约张数，Binance 现货为 BTC。合约张数转换成 BTC 需要另外查询该合约的乘数，本工具不猜测乘数。日线样本可能包含当日尚未完成的 K 线，不能直接视为已清洗的回测数据。

### 规则二：请求头是通与不通的分水岭

大陆的几个金融站点全靠 `Referer` 做防盗链。少一个头就是 403：

| 域名 | 必须的头 |
|---|---|
| `hq.sinajs.cn` | `Referer: https://finance.sina.com.cn` |
| `query.sse.com.cn` | `Referer: http://www.sse.com.cn/` |
| `www.szse.cn/api/...` | `Referer: http://www.szse.cn/market/product/stock/list/index.html` |
| `www.cninfo.com.cn/new/...` | `Referer: http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice` + `X-Requested-With: XMLHttpRequest` |
| `data.sec.gov` / `www.sec.gov` | `User-Agent: 你的名字 你的邮箱`（SEC 强制要求，否则 403 并可能封 IP） |

东方财富 `push2.eastmoney.com` / `push2his.eastmoney.com` 不需要 Referer，裸请求就通。这是大陆最省事的一条路。

### 规则三：限速，别把源打死

| 源 | 建议间隔 |
|---|---|
| 东方财富、新浪、腾讯 | ≥ 200 ms/请求，单线程 |
| SEC EDGAR | ≤ 10 req/s（官方上限） |
| CoinGecko 免费版 | ≤ 10-30 req/min |
| Binance REST | 使用请求权重，当前上限以交易所规则和响应头为准 |
| arXiv API | ≥ 3 s/请求（官方要求） |
| OpenAlex | 鉴权与限额以当前官方说明为准，`mailto` 不等于授权密钥 |
| Crossref | 可带 `mailto=` 提供联系信息，遵守响应头的速率限制 |

批量历史数据优先走**打包下载**（Binance Vision zip、SEC full-index、Stooq CSV），不要用逐条 API 硬刷。

---

## 四、四类目标的最短路径

### 币圈日线/分钟线全历史
`data.binance.vision` 的 zip 归档 `[OK]`。公开历史包按月或按日下载，仍应控制并发。见 `reference/data-sources.md` §1.1。
历史检查中 `api.binance.com` 返回过 **451**。可核对 OKX/Gate 等合法可用的来源；不同交易所行情不等价，替换时应记录来源变化。

### A股日线 + 复权
东方财富 `push2his.eastmoney.com/api/qt/stock/kline/get` `[OK]`，或直接 `akshare` `[OK]`。见 §2.1。

### 港股
东方财富 secid 前缀 `116.`（如 `116.00700` = 腾讯）`[OK]`。CCASS 持股走 `www3.hkexnews.hk/sdw` `[OK]`。见 §3。

### 美股
`stooq.com/q/d/l/?s=aapl.us&i=d` 直接吐 CSV `[OK]`；财报走 SEC XBRL API `[OK+H]`。见 §4。

### 论文
arXiv API + Crossref API 提供公开检索，附带 OpenAlex 等索引。各站当前的鉴权和额度需单独核对。见 `reference/papers.md`。

---

## 五、通用抓取骨架

大陆金融站点的最小可用请求，Python 版：

```python
import time, requests  # 此扩展示例另需安装 requests；上面的自带工具不需要它

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/120.0.0.0 Safari/537.36"),
})

# 每个域名需要的额外头，抓取前按域名匹配上去
REFERERS = {
    "hq.sinajs.cn":        "https://finance.sina.com.cn",
    "query.sse.com.cn":    "http://www.sse.com.cn/",
    "www.szse.cn":         "http://www.szse.cn/market/product/stock/list/index.html",
    "www.cninfo.com.cn":   "http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice",
}

def get(url, *, timeout=20, retries=3, sleep=0.25, **kw):
    """带 Referer 自动补全、指数退避重试的 GET。"""
    from urllib.parse import urlparse
    host = urlparse(url).netloc
    headers = dict(kw.pop("headers", {}))
    if host in REFERERS:
        headers.setdefault("Referer", REFERERS[host])
    last = None
    for i in range(retries):
        try:
            r = SESSION.get(url, timeout=timeout, headers=headers, **kw)
            r.raise_for_status()
            time.sleep(sleep)
            return r
        except Exception as exc:      # 429/5xx/网络抖动都退避重试
            last = exc
            time.sleep(sleep * (2 ** i))
    raise RuntimeError("GET failed after %d tries: %s -- %s" % (retries, url, last))
```

需要登录态（雪球、微博、部分券商页面）时可另外评估 Playwright 持久化 profile：先由用户正常登录，
再用 `page.request.get()` 读取已授权接口。这些脚本不在本 Skill 内，当前工具也不读取 cookie。
登录状态包含个人凭据，必须保存在本地排除上传的目录。

---

## 六、法律与合规底线

写爬虫之前读三样东西：目标站的 `robots.txt`、服务条款、以及数据的再分发条款。

- 交易所行情数据（HKEX、SSE、SZSE、NASDAQ）**再分发通常需要授权**，自用研究和对外发布是两回事
- 商业数据库（Wind、CSMAR、CRSP、Compustat、LOBSTER）签的是机构协议，导出数据外传是违约
- 个人账户接口（券商 OpenAPI）有并发和频率硬限制，超了封账号不封 IP
- 不要绕过验证码、不要伪造登录态卖数据、不要把付费源转手

这份索引记录**路径**，用不用、怎么用是使用者的责任。

---

## 七、维护

发现某条失效时，改 `reference/*.md` 里对应行的标记并写上失效日期，不要直接删——删掉后下次有人会重新踩一遍。

新增源时补三样：URL、返回格式、必需请求头。缺任一样的条目对下一个用它的人没有价值。
