# 论文、课程与阅读阶梯

核对日期：`2026-08-11`。

这不是一份“越多越好”的书单。零基础直接逐页啃经典论文，通常只会记住公式而不知道它解决什么问题。正确顺序是先用课程建立概念，再按当前项目读论文。

**论文**是作者对一个明确问题给出的数据、方法、证据和结论。论文不是交易说明书，也不保证结论在今天、在中国市场或扣除成本后仍成立。

## 1. 怎样读一篇论文

每篇分三次读：

1. 第一次只看标题、摘要、数据、主要图表、结论，回答“作者问什么、发现什么”。
2. 第二次看研究方法和限制，回答“怎样得到结论、可能错在哪里”。
3. 第三次才推公式和做最小复现，回答“我能否用另一段数据得到相近结果”。

难度用 `1-5` 表示：`1` 是看摘要和图表即可；`3` 需要基础统计；`5` 需要高等数学、时间序列或市场微观结构。

链接优先给 DOI。**DOI** 是论文的永久数字标识；出版社页面可能只开放摘要或要求付费。不要绕过付费限制，可以从作者主页、SSRN、arXiv、NBER、学校仓库或 Unpaywall 寻找作者合法公开的版本。

## 2. 零基础公开课程

### 第 2-7 周：Python 与数据

| 资料 | 学什么 | 使用方法 |
|---|---|---|
| [Harvard CS50P](https://cs50.harvard.edu/python/) | 从零开始学习 Python、函数、异常和测试 | 免费课程；只完成路线所需部分，不以背语法为目标 |
| [Python 官方教程](https://docs.python.org/3/tutorial/) | 变量、条件、循环、函数、异常 | 不必全部完成；以能读懂项目代码为标准 |
| [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/) | NumPy、pandas、Matplotlib、基础机器学习 | 免费在线书；配合每周数据项目 |
| [pandas 入门教程](https://pandas.pydata.org/docs/getting_started/intro_tutorials/) | 表格、缺失值、分组、时间序列 | 每学一节就换成真实行情小表操作 |

### 第 8-13 周：概率、统计和线性代数

| 资料 | 学什么 | 使用方法 |
|---|---|---|
| [Khan Academy Statistics and Probability](https://www.khanacademy.org/math/statistics-probability) | 概率、分布、抽样、回归和假设检验 | 不会的概念先看直观讲解，再回路线做模拟 |
| [Seeing Theory](https://seeing-theory.brown.edu/) | 用互动图形理解概率、分布、推断和回归 | 先动滑块观察，再写一句自己的解释 |
| [OpenIntro Statistics](https://www.openintro.org/book/os/) | 免费统计教材与练习 | 作为主要统计参考书，不要求一次读完 |
| [MIT 6.041SC Applied Probability](https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/) | 概率模型、条件概率、随机变量和随机过程 | 比 OpenIntro 更偏数学；先完成直观练习再选相关章节 |
| [MIT 18.06 Linear Algebra](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/) | 向量、矩阵、线性方程和特征值 | 组合和机器学习前掌握直觉；“特征值”是矩阵中描述某些稳定方向和缩放程度的数 |
| [Mathematics for Machine Learning](https://mml-book.github.io/) | 线性代数、微积分和概率的机器学习视角 | 免费书；用于补缺，不要求在机器学习前逐页完成 |
| [Forecasting: Principles and Practice](https://otexts.com/fpp3/) | 趋势、季节性、预测误差和时间顺序交叉验证 | 示例使用 R；R 是侧重统计分析的编程语言，概念可以直接迁移到 Python |

### 第 1-17 周：金融与市场

| 资料 | 学什么 | 使用方法 |
|---|---|---|
| [MIT 15.401 Finance Theory I](https://ocw.mit.edu/courses/15-401-finance-theory-i-fall-2008/) | 现值、风险收益、组合、资产定价和期权基础 | 先看讲义和作业题，遇到数学再回统计课程 |
| [Yale ECON 252 Financial Markets](https://oyc.yale.edu/economics/econ-252) | 市场制度、风险、行为金融和主要资产 | Open Yale Courses 页面提供讲座与文字稿；[Coursera 版本](https://www.coursera.org/learn/financial-markets-global) 的注册或旁听规则可能变化 |
| [QuantEcon Lectures](https://quantecon.org/lectures/) | 经济学、概率、动态模型和 Python | 作为长期参考，不按网站顺序全部学习 |

### 第 38-41 周：机器学习

| 资料 | 学什么 | 使用方法 |
|---|---|---|
| [An Introduction to Statistical Learning](https://www.statlearning.com/) | 回归、分类、树模型、重采样和无监督学习 | 免费书；优先读概念、图和实验，不先追求证明 |
| [Georgia Tech CS 7646: Machine Learning for Trading](https://omscs.gatech.edu/cs-7646-machine-learning-trading) | 把机器学习放入交易研究流程 | 官方课程页仍在；当前公开内容需要注册 Ed Lessons 并用邮件激活，旧 Udacity `ud501` 已不是同一门课 |
| [Machine Learning for Trading 代码](https://github.com/stefan-jansen/machine-learning-for-trading) | 数据、特征、模型、成本、回测和部署案例 | 先完成路线中的统计与回测阶段，再选一个案例复现 |

### 第 42 周以后：衍生品与高级金融计算

| 资料 | 学什么 | 使用方法 |
|---|---|---|
| [MIT 18.642 Mathematics with Applications in Finance](https://ocw.mit.edu/courses/18-642-topics-in-mathematics-with-applications-in-finance-fall-2024/) | 金融中的概率、优化、随机过程和衍生品 | 需要概率、微积分和线性代数；期权阶段按主题选学 |
| [MIT 15.450 Analytics of Finance](https://ocw.mit.edu/courses/15-450-analytics-of-finance-fall-2010/) | 金融计量、蒙特卡洛、随机微积分、风险和衍生品 | 高级参考，不适合第一阶段 |

## 3. 第一组：研究可信度，必须最先读

这些论文不直接给“赚钱策略”，却比策略论文更重要。它们解释为什么大量漂亮回测只是偶然。

| 论文 | 难度 / 时间 | 你要带走的结论 |
|---|---|---|
| [Lo, The Statistics of Sharpe Ratios, 2002](https://doi.org/10.2469/faj.v58.n4.2453) | 4 / 第 22 周 | 夏普比率也有抽样误差；收益存在自相关时，不能机械地用时间平方根做年化 |
| [White, A Reality Check for Data Snooping, 2000](https://doi.org/10.1111/1468-0262.00152) | 4 / 第 21 周 | 试过很多规则后，最优结果会有选择偏差；必须把“试了多少次”纳入判断 |
| [Bailey et al., The Probability of Backtest Overfitting, 2016](https://doi.org/10.21314/JCF.2016.322) | 3 / 第 21 周 | 即使没有明显程序错误，反复选择方案也会让样本内赢家在样本外失败；[UC eScholarship 作者版本](https://escholarship.org/uc/item/4w1110bb) 可合法免费阅读 |
| [Bailey & López de Prado, The Deflated Sharpe Ratio, 2014](https://doi.org/10.3905/jpm.2014.40.5.094) | 4 / 第 22 周 | 普通夏普比率没有充分考虑非正态收益、短样本和多次尝试，需要更保守地解释；[SSRN 作者版本](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551) 可免费访问 |
| [Harvey, Liu & Zhu, … and the Cross-Section of Expected Returns, 2016](https://doi.org/10.1093/rfs/hhv059) | 4 / 第 21-23 周 | 大量因子被同时尝试后，传统显著性门槛太宽松；新因子需要更强证据 |
| [McLean & Pontiff, Does Academic Research Destroy Stock Return Predictability?, 2016](https://doi.org/10.1111/jofi.12365) | 3 / 第 23 周 | 许多已发表异常后来减弱，原因可能包括资金进入消除机会，也包括原研究过度拟合 |
| [Arnott, Harvey & Markowitz, A Backtesting Protocol in the Era of Machine Learning, 2019](https://doi.org/10.2139/ssrn.3275654) | 2 / 第 24 周 | 在机器学习时代，研究必须预先写明假设、数据、成本、样本分割和最终检验；SSRN 版本可公开访问 |
| [Frazzini, Israel & Moskowitz, Trading Costs, 2018](https://doi.org/10.2139/ssrn.3229719) | 3 / 第 17、23 周 | 成本取决于交易规模、流动性和执行方式，不能用一个随意常数替代所有现实成本 |

阅读要求：前两周只需要把每篇的研究问题、主要警告和你自己的回测检查项写出来。公式看不懂不影响第一次阅读。

## 4. 第二组：市场、组合与资产定价

**资产定价**研究资产为什么有不同预期收益，以及风险与价格怎样联系。

| 论文 | 难度 / 时间 | 概念、逻辑与应用 |
|---|---|---|
| [Markowitz, Portfolio Selection, 1952](https://doi.org/10.1111/j.1540-6261.1952.tb01525.x) | 3 / 第 33 周 | 概念：不要孤立看一项资产，要看整个组合。逻辑：共同变化程度决定分散效果。应用：比较单资产风险与组合风险 |
| [Sharpe, Capital Asset Prices, 1964](https://doi.org/10.1111/j.1540-6261.1964.tb02865.x) | 4 / 第 33 周 | 概念：市场风险 Beta。逻辑：不能通过分散消除的风险可能要求补偿。应用：检查策略收益是否只是市场上涨 |
| [Fama, Efficient Capital Markets, 1970](https://doi.org/10.2307/2325486) | 3 / 第 1、25 周 | 概念：价格会竞争性地吸收信息。逻辑：公开且容易利用的规律会吸引资金并减弱。应用：每个策略都要回答为什么机会尚未消失 |
| [Black & Litterman, Global Portfolio Optimization, 1992](https://doi.org/10.2469/faj.v48.n5.28) | 4 / 第 34 周 | 概念：把市场隐含预期与研究者观点结合。应用：避免直接使用极不稳定的历史平均收益做优化 |
| [DeMiguel, Garlappi & Uppal, Optimal Versus Naive Diversification, 2009](https://doi.org/10.1093/rfs/hhm075) | 3 / 第 34 周 | 复杂优化在样本外不一定胜过简单 `1/N` 等权；简单基线必须保留 |
| [Moreira & Muir, Volatility-Managed Portfolios, 2017](https://doi.org/10.1111/jofi.12513) | 4 / 第 35 周 | 市场波动高时降低仓位、波动低时提高仓位；要同时检查杠杆、换手和危机反转 |
| [Rockafellar & Uryasev, Optimization of Conditional Value-at-Risk, 2000](https://doi.org/10.21314/JOR.2000.038) | 5 / 第 36 周以后 | 把极端损失超过某个门槛后的平均值写成可优化问题；[University of Washington 作者 PDF](https://sites.math.washington.edu/~rtr/papers/rtr179-CVaR1.pdf) 可免费阅读 |

`1/N` 表示把资金平均分给 `N` 项资产。Beta 是资产相对市场变动的敏感程度；例如 Beta 约为 `1.2`，表示历史上市场变化 `1%` 时，该资产平均同方向变化约 `1.2%`，但这不是未来保证。**Conditional Value-at-Risk** 常缩写为 CVaR，也叫预期损失尾值，表示已经进入最差一段结果以后，平均会损失多少。

## 5. 第三组：因子、价值与动量

| 论文 | 难度 / 时间 | 概念、逻辑与应用 |
|---|---|---|
| [Fama & French, Common Risk Factors in the Returns on Stocks and Bonds, 1993](https://doi.org/10.1016/0304-405X%2893%2990023-5) | 3 / 第 28 周 | 市场、规模和价值三个因子能描述很多股票共同收益变化；用 [Kenneth French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) 做最小复现 |
| [Jegadeesh & Titman, Returns to Buying Winners and Selling Losers, 1993](https://doi.org/10.1111/j.1540-6261.1993.tb04702.x) | 3 / 第 26 周 | 过去中期赢家相对过去输家出现延续；必须处理形成期、持有期、做空与成本 |
| [Asness, Moskowitz & Pedersen, Value and Momentum Everywhere, 2013](https://doi.org/10.1111/jofi.12021) | 3 / 第 28-29 周 | 价值与动量不只出现在美股，也出现在多个资产类别；跨市场相似不等于每时每地都盈利 |
| [Novy-Marx, The Other Side of Value: The Gross Profitability Premium, 2013](https://doi.org/10.1016/j.jfineco.2013.01.003) | 3 / 第 29 周 | 毛利润相对于资产规模可作为质量特征；财务数据必须按当时公开日期使用 |
| [Fama & French, A Five-Factor Asset Pricing Model, 2015](https://doi.org/10.1016/j.jfineco.2014.10.010) | 4 / 第 29 周 | 在市场、规模、价值上加入盈利和投资因子；因子增加后解释力可能提高，也会增加选择空间 |
| [Shleifer & Vishny, The Limits of Arbitrage, 1997](https://doi.org/10.3386/w5167) | 3 / 第 25、30 周 | 即使价格看起来错误，资金、期限和客户赎回限制也可能阻止套利者立即修正它 |

因子论文的第一个项目只做“分组检验”：按因子值把资产分组，比较之后收益。不要一开始就用几十个因子和机器学习挑选最佳组合。

## 6. 第四组：趋势、均值回归与统计套利

| 论文 | 难度 / 时间 | 概念、逻辑与应用 |
|---|---|---|
| [Lo & MacKinlay, Stock Market Prices Do Not Follow Random Walks, 1988](https://doi.org/10.1093/rfs/1.1.41) | 4 / 第 13、27 周 | 用统计检验检查价格变化是否完全像随机游走；拒绝随机游走不等于已经得到可交易策略 |
| [De Bondt & Thaler, Does the Stock Market Overreact?, 1985](https://doi.org/10.1111/j.1540-6261.1985.tb05004.x) | 3 / 第 27 周 | 长期输家之后可能相对反弹，提供过度反应和长期反转证据；需要检查风险、退市样本和持有期 |
| [Moskowitz, Ooi & Pedersen, Time Series Momentum, 2012](https://doi.org/10.1016/j.jfineco.2011.11.003) | 3 / 第 25 周 | 同一资产过去一段时间的方向可能延续；在多类期货中研究趋势，并显式控制风险 |
| [Hurst, Ooi & Pedersen, A Century of Evidence on Trend-Following Investing, 2017](https://doi.org/10.3905/jpm.2017.44.1.015) | 2 / 第 25 周 | 扩展到更长历史检查趋势策略是否只碰巧适合近期；重点读数据限制和成本假设 |
| [Gatev, Goetzmann & Rouwenhorst, Pairs Trading, 2006](https://doi.org/10.1093/rfs/hhj020) | 3 / 第 30 周 | 用历史价格距离寻找配对，价差异常后押注恢复；寻找期与检验期必须分开 |
| [Avellaneda & Lee, Statistical Arbitrage in the US Equities Market, 2010](https://doi.org/10.1080/14697680903124632) | 5 / 第 31 周以后 | 用因子模型分离共同变化，再对残差做均值回归；[NYU 作者 PDF](https://math.nyu.edu/faculty/avellane/AvellanedaLeeStatArb20090616.pdf) 可免费阅读；论文也展示了后期策略衰减 |

趋势与均值回归并不矛盾：同一市场在不同时间尺度上可能同时存在长期趋势和短期反转。必须在提出假设前固定所研究的时间尺度，不能看到结果后再改说法。

## 7. 第五组：机器学习

| 论文 | 难度 / 时间 | 概念、逻辑与应用 |
|---|---|---|
| [Gu, Kelly & Xiu, Empirical Asset Pricing via Machine Learning, 2020](https://doi.org/10.1093/rfs/hhaa009) | 5 / 第 38-41 周 | 比较多种模型预测股票相对收益，强调非线性和变量交互；[作者 PDF](https://dachxiu.chicagobooth.edu/download/ML.pdf) 可免费阅读；先复现简单线性基线，不直接跳深度网络 |
| [Fischer & Krauss, Deep Learning with LSTM Networks for Financial Market Predictions, 2018](https://doi.org/10.1016/j.ejor.2017.11.054) | 4 / 第 41 周以后 | LSTM 是处理顺序数据的神经网络；把它当案例学习数据分割与基线比较，不把单篇结果当普遍盈利证据 |
| [Arnott, Harvey & Markowitz, A Backtesting Protocol](https://doi.org/10.2139/ssrn.3275654) | 2 / 第 38 周再次读 | 机器学习能够更快尝试更多方案，因此比简单策略更需要冻结测试集和记录实验次数 |

**非线性**表示输入变化与输出变化不是固定直线关系。**变量交互**表示一个特征的作用取决于另一个特征。**LSTM** 是长短期记忆网络，属于神经网络；神经网络通过多层计算从数据中学习复杂映射。

## 8. 第六组：期权、执行与高频

| 论文 | 难度 / 时间 | 概念、逻辑与应用 |
|---|---|---|
| [Black & Scholes, The Pricing of Options and Corporate Liabilities, 1973](https://doi.org/10.1086/260062) | 5 / 第 43 周 | 通过动态对冲建立经典期权定价框架；重点理解假设，不要把理论价格当保证成交价 |
| [Merton, Theory of Rational Option Pricing, 1973](https://doi.org/10.2307/3003143) | 5 / 第 43 周以后 | 扩展连续时间期权定价；[MIT 作者工作论文](https://dspace.mit.edu/handle/1721.1/49331) 可免费阅读 |
| [Engle, Autoregressive Conditional Heteroscedasticity, 1982](https://doi.org/10.2307/1912773) / [Bollerslev, Generalized ARCH, 1986](https://doi.org/10.1016/0304-4076%2886%2990063-1) | 5 / 第 44 周以后 | ARCH/GARCH 让当前波动随过去冲击和过去波动变化，用来描述“大波动之后常跟着大波动” |
| [Heston, A Closed-Form Solution for Options with Stochastic Volatility, 1993](https://doi.org/10.1093/rfs/6.2.327) | 5 / 第 44 周以后 | 让波动率自身随机变化，解释部分期权价格形状；完成微积分和 Black-Scholes 后再读 |
| [Cboe VIX Mathematics Methodology](https://cdn.cboe.com/resources/indices/Cboe_Volatility_Index_Mathematics_Methodology.pdf) | 4 / 第 44 周 | 官方方法文档，说明 VIX 怎样用一组期权价格估计未来约 30 天的隐含波动率 |
| [Kyle, Continuous Auctions and Insider Trading, 1985](https://doi.org/10.2307/1913210) | 5 / 第 45 周以后 | 研究知情交易者、流动性提供者与价格冲击怎样共同决定价格 |
| [Glosten & Milgrom, Bid, Ask and Transaction Prices, 1985](https://doi.org/10.1016/0304-405X%2885%2990044-3) | 5 / 第 45 周以后 | 信息不对称会让流动性提供者面临不利成交，从而形成部分买卖价差 |
| [Almgren & Chriss, Optimal Execution of Portfolio Transactions, 2001](https://doi.org/10.21314/JOR.2001.041) | 5 / 第 46 周以后 | 在市场冲击与价格风险之间选择订单执行速度；适合成交算法专题 |
| [Avellaneda & Stoikov, High-Frequency Trading in a Limit Order Book, 2008](https://doi.org/10.1080/14697680701381228) | 5 / 第 46 周以后 | 做市商根据库存和风险调整买卖报价；[NYU 作者 PDF](https://math.nyu.edu/faculty/avellane/HighFrequencyTrading.pdf) 可免费阅读；模型假设比公式结果更重要 |

**动态对冲**是随着标的价格和时间变化不断调整对冲仓位。**随机波动率**表示市场波动程度本身也会随机变化。**波动率聚集**表示大幅波动之后更容易继续出现大幅波动。**VIX** 是 Cboe 根据标普 500 指数期权价格计算的预期波动指标；Cboe 是运营期权交易所和指数的市场机构，标普 500 是代表美国大型上市公司的常用股票指数。VIX 常被称为“恐慌指数”，但它不是对未来涨跌方向的预测。**信息不对称**表示交易双方掌握的信息不同。**价格冲击**是自己的订单推动市场价格向不利方向变化。

## 9. 第七组：加密货币专题

加密货币放在通用研究方法之后。市场全天交易、交易所分散、历史较短、规则和交易对手风险不同，不能把股票结论直接搬过去。

| 论文 | 难度 / 时间 | 概念、逻辑与应用 |
|---|---|---|
| [Liu & Tsyvinski, Risks and Returns of Cryptocurrency, 2021](https://doi.org/10.1093/rfs/hhaa113) | 3 / 通用路线完成后 | 研究加密收益与传统风险、动量和投资者关注度的关系 |
| [Liu, Tsyvinski & Wu, Common Risk Factors in Cryptocurrency, 2022](https://doi.org/10.1111/jofi.13119) | 4 / 通用路线完成后 | 构造加密市场、规模和动量等共同因子；短历史和交易所差异必须单独检查 |
| [Makarov & Schoar, Trading and Arbitrage in Cryptocurrency Markets, 2020](https://doi.org/10.1016/j.jfineco.2019.07.001) | 4 / 通用路线完成后 | 不同交易所的价格差揭示跨境资金和结算限制；看到价差不等于能无风险成交 |

**交易对手风险**是对方交易所、托管方或借贷方不能履约造成损失的风险。

## 10. 论文网站怎样分工

| 网站 | 是什么 | 怎样用 |
|---|---|---|
| [DOI Resolver](https://doi.org/) | 根据永久标识跳到论文正式页面 | 已知 DOI 时最稳定的入口 |
| [Google Scholar](https://scholar.google.com/) | 学术搜索引擎 | 找题目、引用和作者公开版本；搜索结果不是质量认证 |
| [Semantic Scholar](https://www.semanticscholar.org/) | 提供论文关系、摘要和引用的搜索系统 | 用来发现相关论文，再回正式来源核对 |
| [OpenAlex](https://openalex.org/) | 开放的学术作品、作者和机构目录 | 查询元数据和开放版本，记录可能不完整 |
| [Crossref Search](https://search.crossref.org/) | DOI 注册信息搜索 | 核对标题、作者、年份和 DOI |
| [SSRN Financial Economics](https://www.ssrn.com/index.cfm/en/finrn/) | 金融、经济、法律等工作论文平台 | 很多论文可免费读；自动访问可能触发限制，普通浏览器使用即可；工作论文可能尚未同行评审 |
| [arXiv q-fin](https://arxiv.org/list/q-fin/recent) | 量化金融预印本列表 | `PM` 偏组合、`ST` 偏统计金融、`RM` 偏风险、`TR` 偏交易与微观结构；免费不等于已同行评审 |
| [NBER Asset Pricing](https://www.nber.org/programs-projects/programs-working-groups/asset-pricing) | 美国国家经济研究局资产定价工作论文 | 摘要通常可读，下载权限不统一；工作论文与最终期刊版可能不同 |
| [IDEAS/RePEc](https://ideas.repec.org/) | 经济学论文、作者和机构索引 | 找工作论文与不同版本，不负责统一审查质量 |
| [CORE](https://core.ac.uk/) | 聚合大学和研究机构开放论文 | 用 DOI 或完整标题寻找合法公开版本 |
| [Unpaywall Simple Query Tool](https://unpaywall.org/products/simple-query-tool) | 根据 DOI 查找合法开放版本 | 出版社页面收费时，用它找作者或机构已公开的版本 |

**工作论文**是仍在研究和修改中的公开版本。**预印本**是正式同行评审前公开的稿件。两者都可以很有价值，但引用时要记录版本和日期。

## 11. 最小必读清单

如果一年内只精读十二篇，按下面顺序：

1. Fama, *Efficient Capital Markets*。
2. Bailey et al., *The Probability of Back-Test Over-Fitting*。
3. Arnott et al., *A Backtesting Protocol in the Era of Machine Learning*。
4. Frazzini et al., *Trading Costs*。
5. Markowitz, *Portfolio Selection*。
6. DeMiguel et al., *Optimal Versus Naive Diversification*。
7. Fama & French, *Common Risk Factors*。
8. Jegadeesh & Titman, *Returns to Buying Winners and Selling Losers*。
9. Moskowitz et al., *Time Series Momentum*。
10. Gatev et al., *Pairs Trading*。
11. Gu et al., *Empirical Asset Pricing via Machine Learning*。
12. Almgren & Chriss, *Optimal Execution*。

这十二篇不是十二套可以直接下单的策略，而是一条完整研究链：市场为什么难预测、怎样避免假结果、成本怎样进入、策略证据怎样形成、组合怎样控制风险、模型怎样验证、订单最后怎样成交。
