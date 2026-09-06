# 算法索引：公开经典 + 当前前沿

分四层：因子构造 → 预测建模 → 组合与风险 → 执行与微观结构。每层给出方法、代表实现、代码入口。

标记见 `../SKILL.md` §二。实测时间 2026-09-01。

---

## 0. 一句话选型

| 你的情况 | 直接用 |
|---|---|
| A股日频多因子，想要一整套流水线 | **Qlib**（微软），数据+特征+模型+回测全包 |
| 想自动挖公式因子 | **gplearn** / **AlphaGen** / Qlib 的 `Alpha158`/`Alpha360` |
| 币圈高频、要低延迟回测 | **NautilusTrader** |
| 币圈策略快速上线 | **Freqtrade** |
| A股实盘接券商 | **vn.py** |
| 只想验证因子有效性 | **Alphalens** + Kenneth French 因子基准 |
| LOB 深度学习 | **DeepLOB** 系列 + LOBSTER / Databento MBO 数据 |

---

## 1. 因子构造（Alpha 挖掘）

### 1.1 公开因子集（拿来就能算）

| 因子集 | 数量 | 来源 | 备注 |
|---|---|---|---|
| **WorldQuant 101 Alphas** | 101 | Kakushadze (2015), arXiv:1601.00991 | 公式全部公开，是所有公式因子研究的基线 |
| **Qlib Alpha158** | 158 | Qlib 内置 | 价量衍生，`qlib.contrib.data.handler.Alpha158` |
| **Qlib Alpha360** | 360 | Qlib 内置 | 原始价量 60 日窗口展开，适合喂神经网络 |
| **Fama-French 3/5** | 3/5 | French Data Library | 学术基准，必须作为对照组 |
| **Barra CNE5/6** | ~40 | MSCI 商业模型 | 结构公开，实现需自建；国内券商普遍复刻 |
| **Liu-Stambaugh-Yuan** | 3/4 | JFE 2019 | 中国版三因子，剔除小市值壳股，A股研究应优先于 FF3 |
| **q-factor / q5** | 4/5 | Hou-Xue-Zhang | 投资 + ROE 因子 |

WorldQuant 101 的 Python 实现参考：
```
https://github.com/yli188/WorldQuant_alpha101_code   # 常见实现
Qlib 也可用表达式引擎直接写：
  "Corr($close, Log($volume+1), 10)"
  "Rank($close/Ref($close,5)-1)"
```

### 1.2 遗传编程 / 符号回归自动挖因子

| 工具 | 地址 | 状态 |
|---|---|---|
| **gplearn** | `https://gplearn.readthedocs.io/en/stable/` | `[OK]` 最经典的 GP 符号回归，改 `function_set` 加金融算子即可 |
| DEAP | `https://deap.readthedocs.io/` | 通用进化计算，灵活但要自己搭 |
| **AlphaGen** | `https://github.com/RL-MF/alphagen`（Yu et al., KDD 2023） | 强化学习挖公式因子，显式优化因子组合 IC 而非单因子 |
| AutoAlpha | Zhang et al. 2020 | 层次化搜索，减少冗余因子 |
| **AlphaForge** | Shi et al., AAAI 2024 | 生成-预测神经架构挖因子，当前公式因子挖掘 SOTA 之一 |

gplearn 用于因子挖掘的关键改造：
```python
from gplearn.genetic import SymbolicTransformer
from gplearn.functions import make_function
import numpy as np

def _ts_rank(x):          # 时序排名，金融特有算子
    return np.argsort(np.argsort(x)) / max(len(x) - 1, 1)

ts_rank = make_function(function=_ts_rank, name='ts_rank', arity=1)

gp = SymbolicTransformer(
    generations=20, population_size=2000, hall_of_fame=100,
    n_components=20,
    function_set=['add', 'sub', 'mul', 'div', 'sqrt', 'log', 'abs', ts_rank],
    metric='spearman',            # 用 rank IC 而非 MSE
    parsimony_coefficient=0.001,  # 抑制表达式膨胀
    random_state=42,
)
```
两个坑：`metric` 必须用 rank 相关而不是 MSE（金融信号看序不看值）；`parsimony_coefficient` 太小会长出无法解释的巨型表达式，过拟合极严重。

### 1.3 因子评估

**Alphalens** `[OK]` `https://github.com/quantopian/alphalens`
分位数收益、IC 时序、换手率、行业中性化后的表现，一份 tear sheet 全出。Quantopian 已停运但代码可用，活跃分支是 `alphalens-reloaded`。

必看的四个数：
- **IC / rank IC 均值**：日频 > 0.03 算有信号
- **ICIR**（IC 均值 / IC 标准差）：> 0.3 才算稳定
- **换手率**：高换手因子在 A股会被印花税和冲击成本吃掉
- **分位单调性**：不单调说明因子非线性，直接线性加权会失效

---

## 2. 预测建模

### 2.1 树模型（横截面收益预测的实际最强基线）

| 模型 | 库 | 备注 |
|---|---|---|
| LightGBM | `lightgbm` | Qlib 里的默认强基线，A股日频常年打不过 |
| XGBoost | `xgboost` | 同上 |
| CatBoost | `catboost` | 类别特征（行业、板块）处理最好 |
| Random Forest | `sklearn` | 稳但弱 |

Gu-Kelly-Xiu (2020, RFS) 用 60 年美股数据比较了 OLS/PLS/PCR/弹性网/GBRT/随机森林/神经网络，结论是**树模型和浅层神经网络显著优于线性模型**，且收益主要来自捕捉非线性交互。这是资产定价机器学习的奠基性实证，任何新方法都要跟它比。

### 2.2 时序深度学习

| 架构 | 论文/来源 | 定位 |
|---|---|---|
| LSTM / GRU | — | 最基础的序列基线 |
| **ALSTM** | Qiu et al. 2020 | 带注意力的 LSTM，Qlib 内置 |
| **GATs** | Velickovic et al. | 股票关系图注意力，Qlib 内置 |
| **TFT** | Lim et al. 2021, IJF | Temporal Fusion Transformer，多时域可解释注意力 |
| **Informer** | Zhou et al., AAAI 2021 Best Paper | ProbSparse 注意力，长序列 O(L log L) |
| **Autoformer** | Wu et al., NeurIPS 2021 | 序列分解 + 自相关机制 |
| **FEDformer** | Zhou et al., ICML 2022 | 频域增强 |
| **PatchTST** | Nie et al., ICLR 2023 | 分块 + 通道独立，长期预测强基线 |
| **DLinear / NLinear** | Zeng et al., AAAI 2023 | 一层线性打败多数 Transformer，**是必须跑的对照组** |
| **iTransformer** | Liu et al., ICLR 2024 | 倒置维度，变量当 token |
| **TimesNet** | Wu et al., ICLR 2023 | 2D 变换捕捉多周期 |
| **Mamba / S4** | Gu & Dao 2023 | 状态空间模型，长序列线性复杂度 |

**关键警告**：DLinear 那篇（*Are Transformers Effective for Time Series Forecasting?*）表明很多 Transformer 在时序预测上的增益来自实验设置而非架构。做金融预测时，**先跑 DLinear 和 LightGBM 当底线**，跑不过就别谈架构创新。

统一实现库：
```
https://github.com/thuml/Time-Series-Library      # 上述架构大部分都有
https://github.com/Nixtla/neuralforecast          # 生产级
https://github.com/unit8co/darts                  # API 友好
```

### 2.3 图神经网络（股票关联建模）

思路：股票不独立，供应链、行业、股东、新闻共现构成图。

| 模型 | 来源 |
|---|---|
| **HATS** | Kim et al. 2019，层次化图注意力 |
| **RSR / Temporal Graph Conv** | Feng et al. 2019, TOIS，关系排序 |
| **HIST** | Xu et al. 2021，挖掘概念驱动的共同趋势 |
| **THGNN** | Xiang et al., CIKM 2022，时序异质图 |
| **MASTER** | Li et al., AAAI 2024，市场引导的股票 Transformer |

A股的图构建实操：申万行业 + 概念板块（东财 `m:90+t:3`）+ 十大股东重叠 + 龙虎榜席位共现。数据都在 `data-sources.md` 里。

### 2.4 强化学习

| 方向 | 代表 |
|---|---|
| 组合管理 | Jiang et al. 2017（EIIE 架构，加密货币组合）；FinRL 框架 |
| 最优执行 | Nevmyvaka et al. 2006（RL 做 VWAP 拆单）；Hendricks & Wilcox 2014 |
| 做市 | Spooner et al. 2018；Ganesh et al. 2019 |
| 因子挖掘 | AlphaGen (KDD 2023) |

框架：
```
FinRL:        https://github.com/AI4Finance-Foundation/FinRL
ElegantRL:    https://github.com/AI4Finance-Foundation/ElegantRL
Stable-Baselines3: 通用 RL，配自建 gym 环境
```

**RL 在金融的真实处境要说清楚**：样本效率低、非平稳环境下策略漂移严重、回测里的成交假设通常过于乐观。论文成绩和实盘表现差距在所有 ML 金融方向里最大。适合做执行优化（有明确即时反馈）而非方向预测。

### 2.5 LLM 与另类数据（2023 年后的主要增量）

| 工作 | 内容 |
|---|---|
| **BloombergGPT** (2023) | 500 亿参数金融专用 LLM，训练数据 51% 金融语料 |
| **FinGPT** | `https://github.com/AI4Finance-Foundation/FinGPT` 开源金融 LLM，LoRA 微调情绪分析 |
| **FinBERT** | Araci 2019 / Yang et al. 2020，金融文本情绪分类，仍是性价比最高的落地选择 |
| **Can ChatGPT Forecast Stock Price Movements?** | Lopez-Lira & Tang (2023)，用 GPT 读新闻头条预测次日收益，报告显著预测力 |
| **FinMem / FinAgent / TradingAgents** | LLM agent 做交易决策，带记忆和反思模块 |
| **StockAgent / FinRobot** | 多 agent 模拟市场 |

中文金融 NLP 资源：
```
研报文本:   巨潮/东财公告 PDF（见 data-sources.md §2.4）
互动易问答: http://irm.cninfo.com.cn/
股吧情绪:   guba.eastmoney.com（爬取需限速，反爬较强）
FinBERT 中文: https://huggingface.co/models?search=finbert%20chinese
```

**LLM 用于金融预测的核心陷阱是 look-ahead bias**：模型预训练语料的截止时间晚于你的回测起点，它「记得」结果。用 LLM 做历史回测时，必须确认模型训练截止日早于测试样本，或改用严格时点的新闻数据 + 只做当期推理。

---

## 3. 组合优化与风险

| 方法 | 来源 | 实现 |
|---|---|---|
| 均值-方差 | Markowitz 1952 | `cvxpy`、`PyPortfolioOpt` |
| Black-Litterman | 1992 | `PyPortfolioOpt` |
| 风险平价 / 层次风险平价 | Lopez de Prado 2016 | `riskfolio-lib`、`PyPortfolioOpt` |
| **HRP**（层次聚类做权重） | Lopez de Prado, JPM 2016 | 不需要矩阵求逆，对协方差估计误差稳健 |
| Ledoit-Wolf 收缩协方差 | 2004 | `sklearn.covariance.LedoitWolf` |
| 去噪协方差（RMT） | Lopez de Prado 2020 | `mlfinlab` 的 detoning |
| Kelly / 增长最优 | Kelly 1956, Thorp | 全 Kelly 波动过大，实务用分数 Kelly |
| CVaR 优化 | Rockafellar-Uryasev 2000 | `riskfolio-lib` |

库：
```
PyPortfolioOpt:  https://pyportfolioopt.readthedocs.io/
riskfolio-lib:   https://riskfolio-lib.readthedocs.io/
cvxpy:           凸优化底座，带约束的组合问题都能表达
```

### 回测方法论（比模型更容易出问题的地方）

Lopez de Prado 的 *Advances in Financial Machine Learning* (2018) 是这一块的标准参考，核心几件事：

| 问题 | 解法 |
|---|---|
| **标签泄漏**（重叠样本） | Purged K-Fold + Embargo |
| **固定时间采样低效** | Dollar bars / Volume bars / Imbalance bars |
| **固定持有期标签失真** | Triple-Barrier Labeling（止盈/止损/时间三重边界） |
| **样本权重错误** | Uniqueness weighting（按标签重叠度降权） |
| **多重检验虚假发现** | Deflated Sharpe Ratio、PBO（回测过拟合概率） |
| **特征重要性不可靠** | MDA (Mean Decrease Accuracy) 而非 MDI |

实现：`mlfinlab`（部分闭源）、`https://github.com/hudson-and-thames/mlfinlab`

**Deflated Sharpe Ratio 值得单独强调**：如果你试了 1000 个策略选出 Sharpe 2.0 的那个，它的真实期望 Sharpe 远低于 2.0。不做多重检验校正的回测结果基本不可信。

---

## 4. 执行与市场微观结构

### 4.1 经典执行算法

| 算法 | 论文 | 要点 |
|---|---|---|
| **Almgren-Chriss** | 2000, J. Risk | 最优执行的封闭解，冲击成本 + 时间风险的权衡，所有 VWAP/TWAP 算法的理论基础 |
| Obizhaeva-Wang | 2013 | 引入订单簿弹性恢复 |
| **Kyle 模型** | 1985, Econometrica | λ（Kyle lambda）= 价格冲击系数，流动性度量的标准 |
| Glosten-Milgrom | 1985 | 信息不对称下的买卖价差 |
| **Avellaneda-Stoikov** | 2008 | 做市最优报价，库存风险 + 逆向选择，加密做市机器人的通用起点 |
| Amihud illiquidity | 2002 | \|收益\|/成交额，最易计算的流动性代理 |
| **VPIN** | Easley-Lopez de Prado-O'Hara 2012 | 成交量同步的知情交易概率 |
| Hasbrouck 信息份额 | 1995 | 多市场价格发现归属 |

### 4.2 限价订单簿深度学习

| 模型 | 来源 | 备注 |
|---|---|---|
| **DeepLOB** | Zhang, Zohren, Roberts 2019, IEEE TSP | CNN + Inception + LSTM，LOB 中期价格预测的标准基线 |
| **DeepLOB-Attention** | 2021 | 加注意力 |
| **TransLOB** | Wallbridge 2020 | Transformer 版 |
| **Multi-Horizon LOB** | Zhang & Zohren 2021 | 多时域联合预测 |
| **HLOB** | Briola et al. 2024 | 引入信息过滤网络的层次结构 |
| Benchmark 数据集 | **FI-2010**（Ntakaris et al. 2018） | 芬兰股票 LOB 公开基准，所有 LOB 论文的对照 |

数据来源：LOBSTER（NASDAQ ITCH 重构）、Databento MBO、Tardis（加密全档）。见 `data-sources.md`。

**LOB 研究的三个陷阱**：
1. FI-2010 的标签用了未来中间价，训练集测试集按时间切分才有意义
2. 加密和股票的 LOB 统计性质差异极大（无涨跌停、24h、tick size 相对更小），模型不能直接迁移
3. 预测 tick 级方向的准确率提升往往吃不掉手续费，必须做净收益评估

### 4.3 波动率与期权

| 模型 | 备注 |
|---|---|
| GARCH 族（GARCH/EGARCH/GJR） | `arch` 库，仍是波动率预测的强基线 |
| **HAR-RV** | Corsi 2009，已实现波动率的日/周/月分解，简单且极难被打败 |
| **Rough Volatility** | Gatheral-Jaisson-Rosenbaum 2018，H≈0.1，粗糙路径 |
| **rBergomi** | Bayer-Friz-Gatheral 2016，粗糙随机波动率定价 |
| Heston | 半解析随机波动率 |
| SABR | 利率与外汇市场标准 |
| **Deep Hedging** | Buehler et al. 2019, Quant. Finance，用神经网络直接学对冲策略，不依赖模型假设 |
| **Deep Calibration** | Horvath-Muguruza-Tomas 2021，神经网络加速 rough vol 校准 |
| Neural SDE | Cuchiero et al. 2020 |

库：`arch`、`QuantLib-Python`、`https://github.com/tpq/deep-hedging`

---

## 5. 开源框架汇总

| 框架 | 地址 | 状态 | 适用 |
|---|---|---|---|
| **Qlib** | `https://github.com/microsoft/qlib` / 文档 `https://qlib.readthedocs.io/` | `[OK]` | A股/美股量化全流水线，内置 30+ 模型、Alpha158/360、嵌套回测。**做 A股 ML 因子首选** |
| **vn.py** | `https://github.com/vnpy/vnpy` | `[OK]` | 中国实盘，接 CTP/券商/加密，含 CTA/期权/算法交易模块 |
| **Backtrader** | `https://www.backtrader.com/docu/` | `[OK]` | 单标的策略回测，文档全，社区大 |
| **NautilusTrader** | `https://nautilustrader.io/docs/latest/` | `[OK]` | Rust 内核，事件驱动，纳秒精度，回测代码可直接上实盘 |
| **Freqtrade** | `https://www.freqtrade.io/en/stable/` | `[OK]` | 加密现货/合约，自带下载器 + hyperopt + FreqAI（内置 ML） |
| **Hummingbot** | `https://hummingbot.org/` | `[OK]` | 做市/套利 |
| **CCXT** | `https://docs.ccxt.com/` | `[OK]` | 交易所统一接口层 |
| **Alphalens** | `https://github.com/quantopian/alphalens` | `[OK]` | 因子分析 |
| Zipline-reloaded | `https://github.com/stefan-jansen/zipline-reloaded` | — | Quantopian 引擎的维护分支 |
| **RQAlpha** | `https://github.com/ricequant/rqalpha` | `[OK]` | 米筐开源回测引擎，A股规则贴合度高 |
| **FinRL** | `https://github.com/AI4Finance-Foundation/FinRL` | — | RL 金融全套 |
| **mlfinlab** | `https://github.com/hudson-and-thames/mlfinlab` | — | Lopez de Prado 方法论实现 |
| **PyPortfolioOpt** | `https://pyportfolioopt.readthedocs.io/` | — | 组合优化 |
| **arch** | `https://arch.readthedocs.io/` | — | GARCH 族 |
| **statsmodels** | — | — | 时序检验、协整、Newey-West |
| **QuantLib-Python** | — | — | 衍生品定价与利率曲线 |

### Qlib 最短上手路径

```bash
pip install pyqlib
# A股日线数据（社区维护的镜像）
python -m qlib.run.get_data qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn
```

```python
import qlib
from qlib.constant import REG_CN
from qlib.contrib.data.handler import Alpha158
from qlib.contrib.model.gbdt import LGBModel
from qlib.utils import init_instance_by_config

qlib.init(provider_uri="~/.qlib/qlib_data/cn_data", region=REG_CN)

handler = Alpha158(instruments="csi300",
                   start_time="2015-01-01", end_time="2024-12-31",
                   fit_start_time="2015-01-01", fit_end_time="2020-12-31")

# 训练/验证/测试按时间严格切分，避免泄漏
dataset = init_instance_by_config({
    "class": "DatasetH", "module_path": "qlib.data.dataset",
    "kwargs": {"handler": handler,
               "segments": {"train": ("2015-01-01", "2020-12-31"),
                            "valid": ("2021-01-01", "2022-12-31"),
                            "test":  ("2023-01-01", "2024-12-31")}},
})

model = LGBModel(loss="mse", learning_rate=0.05, num_leaves=64,
                 early_stopping_rounds=50, num_boost_round=1000)
model.fit(dataset)
pred = model.predict(dataset)
```

Qlib 的表达式引擎可以直接写因子，不用手写 pandas：
```
$close / Ref($close, 5) - 1                  # 5 日动量
Mean($volume, 20) / Mean($volume, 60)        # 量比
Corr($close, Log($volume + 1), 10)           # 价量相关
(Max($high, 20) - $close) / Max($high, 20)   # 距 20 日高点
Std($close / Ref($close, 1) - 1, 20)         # 20 日波动
```

---

## 6. A股特有的算法约束

写模型前必须在数据处理里体现，否则回测全是假的：

| 约束 | 影响 | 处理 |
|---|---|---|
| **T+1** | 当日买入次日才能卖 | 回测引擎必须支持，Backtrader 默认不支持需改 |
| **涨跌停** | 封板无法成交 | 涨停不能买、跌停不能卖，信号要过滤 |
| **停牌** | 数据缺失 | 停牌期不计收益，复牌首日不能按前收计算 |
| **印花税 + 佣金** | 卖出 0.05%（2023 减半后）+ 双边佣金 | 高换手因子净收益骤降 |
| **小市值/壳股** | ST 股和微盘股会主导因子收益 | 用 Liu-Stambaugh-Yuan 的做法剔除市值最小 30% |
| **IPO 与次新** | 上市初期价格失真 | 剔除上市 60 日内 |
| **复权** | 不复权会在分红日产生假跌 | 一律用前复权做信号，后复权做净值 |
| **成分股变更** | 生存偏差 | 用时点成分股（point-in-time），不能用今天的沪深300回测五年前 |
| **财报时点** | 用了未公布的财报 = 泄漏 | 用公告日而非报告期，Tushare 的 `ann_date` 字段 |

**币圈对应约束**：24h 无收盘、交易所间价差、资金费率对永续持仓的侵蚀、稳定币脱锚、下架币的生存偏差、交易所自身倒闭（FTX）导致的数据断裂。

---

## 7. 前沿方向速览（2023 年后）

| 方向 | 代表工作 | 成熟度 |
|---|---|---|
| LLM agent 交易 | TradingAgents, FinMem, FinAgent | 早期，回测方法论普遍不严谨 |
| 时序基础模型 | TimeGPT, Chronos (Amazon), Moirai, TimesFM (Google) | 零样本预测能力在金融上尚未证明超越本地训练 |
| 生成式市场模拟 | Diffusion / GAN 生成 LOB 与价格路径，用于数据增强和压力测试 | 活跃 |
| 因果推断 | 双重机器学习 (Chernozhukov et al.)、合成控制用于事件研究 | 学界主流化 |
| Rough volatility | 已进入实务定价 | 成熟 |
| 神经网络资产定价 | Chen-Pelger-Zhu (2024, JF)《Deep Learning in Asset Pricing》，GAN + 深度网络估 SDF | 顶刊已认可 |
| 可解释性 | SHAP/IG 用于因子归因，监管合规驱动 | 落地需求强 |
| 联邦学习 | 多机构数据不出域联合建模 | 概念阶段 |
| 量子优化 | 组合优化 QAOA | 远期 |

---

## 8. 一条务实的判断标准

任何算法在采纳前，问四个问题：

1. **跟最简单的基线比过了吗？** 对时序是 DLinear 和 naive persistence，对横截面是 LightGBM + Alpha158，对波动率是 HAR-RV。打不过就是没有价值。
2. **样本外是怎么切的？** 随机 K-fold 在时序数据上等于泄漏。必须按时间切，且做 purge + embargo。
3. **交易成本算进去了吗？** 换手率 × 双边成本。A股高频因子在扣费后普遍归零。
4. **试了多少个变体才得到这个结果？** 报 Deflated Sharpe 而不是 Sharpe。

绝大多数「新算法在金融上有效」的声明死在第 2 和第 4 条上。
