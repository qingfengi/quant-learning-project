# 论文索引：检索路径与必读清单

以下为公开入口，接口 URL 予以保留。服务商的鉴权、额度和可达性可能变化；这些链接不代表持续免费或持续可用。自带工具仅实现 arXiv 与 Crossref 的小样本检索。

## 1. arXiv（首选，API 完全开放）
- 列表: https://arxiv.org/list/q-fin/recent
- API: https://export.arxiv.org/api/query?search_query=all:stock+prediction&max_results=5

## 2. Crossref（有 DOI 的一切都可查）
- API: https://api.crossref.org/works?rows=5&query=quantitative+trading

## 3. OpenAlex（引文图谱，鉴权与额度以当前官方政策为准）
- API: https://api.openalex.org/works?search=stochastic+volatility&per-page=5&mailto=you@example.com

## 4. Semantic Scholar（免费 API，严格遵守批次大小）
- API: https://api.semanticscholar.org/graph/v1/paper/search?query=limit+order+book&limit=3

## 中文数据库
- 知网 CNKI: https://www.cnki.net/
- 万方: https://www.wanfangdata.com.cn/
- 维普 CQVIP: https://www.cqvip.com/

## 分主题必读核心文献
### 资产定价 × 机器学习
- Gu, Kelly, Xiu (2020) RFS, Empirical Asset Pricing via Machine Learning

### 时间序列深度学习
- Lim et al., TFT; Zhou et al., Informer; Nie et al., PatchTST; Wu et al., TimesNet

### 高频/订单簿
- Zhang et al., DeepLOB; Cont et al., LOB 统计性质

### 回测严谨性
- Lopez de Prado, Advances in Financial ML
