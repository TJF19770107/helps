# 面板体检报告（自动生成）

- 生成时间：2026-11-02T10:54:45.511972+00:00
- 粒度：1D｜品种：76｜日期：2019-11-27 ~ 2026-10-26（2526 天）

## 一、三态总账（并集+填充必须拆开算）

| 状态 | 格数 | 占比 | 处理方式 |
|---|---:|---:|---|
| 真实 bar | 52326 | 27.26% | 正常参与 |
| 未上市缺失 | 139024 | 72.42% | 安全，保持 NaN 不得填充 |
| 上市后断档 | 10 | 0.01% | 标记，因子计算时按缺失处理 |
| 尾部冻结 | 616 | 0.32% | **严禁交易**，tradable_mask=False |

## 二、截面宽度漂移

- 每日品种数：min=1 / p05=6 / median=10 / p95=72 / max=76
- 首日 2019-11-27 仅 1 个品种，末日 2026-10-26 有 6 个
- 宽度 ≥ 中位一半的日期占比：**97.0%**

> 截面宽度随时间从个位数涨到 70+，意味着 `rank`/`zscore` 这类截面因子的**分母在变**。
> 同一个因子值在 2020 年和 2026 年不可比。这是比存活偏差更隐蔽的一层偏差，
> 任何跨期 IC 结论都必须先按宽度分层。

## 三、分层结果

### 长历史层（≥1000 天，11 个）

| 品种 | 首日 | 末日 | 跨度(天) | 真实bar | 断档 | 尾部冻结 |
|---|---|---|---:|---:|---:|---:|
| BTCUSDT | 2020-01-01 | 2026-10-22 | 2486 | 2487 | 0 | 4 |
| ETHUSDT | 2019-11-27 | 2026-09-04 | 2473 | 2474 | 0 | 52 |
| DASHUSDT | 2020-02-04 | 2026-10-22 | 2452 | 2453 | 0 | 4 |
| ZECUSDT | 2020-02-05 | 2026-10-22 | 2451 | 2447 | 5 | 4 |
| BNBUSDT | 2020-02-10 | 2026-10-22 | 2446 | 2447 | 0 | 4 |
| IOSTUSDT | 2020-02-21 | 2026-10-22 | 2435 | 2436 | 0 | 4 |
| DOGEUSDT | 2020-07-10 | 2026-09-04 | 2247 | 2248 | 0 | 52 |
| GTCUSDT | 2021-06-11 | 2026-10-22 | 1959 | 1955 | 5 | 4 |
| QNTUSDT | 2022-10-20 | 2026-10-22 | 1463 | 1464 | 0 | 4 |
| MAGICUSDT | 2023-01-25 | 2026-10-22 | 1366 | 1367 | 0 | 4 |
| LSKUSDT | 2024-01-25 | 2026-10-22 | 1001 | 1002 | 0 | 4 |

### 短历史层（65 个，仅稳健性检验）

PIXELUSDT(980d), STRKUSDT(975d), PORTALUSDT(966d), REZUSDT(905d), SYNUSDT(797d), BANANAUSDT(750d), AVAUSDT(678d), TRUMPUSDT(642d), MELANIAUSDT(640d), VTHOUSDT(638d), HEIUSDT(616d), PIPPINUSDT(588d), BMTUSDT(584d), MUBARAKUSDT(584d), BANANAS31USDT(583d), TUTUSDT(581d), BRUSDT(580d), SIRENUSDT(579d), BANKUSDT(552d), DOODUSDT(531d), AGTUSDT(520d), SOONUSDT(517d), HYPEUSDT(510d), BULLAUSDT(475d), TACUSDT(464d), VELVETUSDT(464d), MYXUSDT(443d), USELESSUSDT(433d), BTRUSDT(421d), HEMIUSDT(419d), QUSDT(415d), ARIAUSDT(414d), FLOCKUSDT(408d), UBUSDT(405d), ASTERUSDT(398d), BLESSUSDT(394d), AKEUSDT(391d), LIGHTUSDT(390d), TRUTHUSDT(386d), EVAAUSDT(384d), 4USDT(379d), RIVERUSDT(374d), LABUSDT(370d), USDT(367d), UAIUSDT(354d), JCTUSDT(346d), BEATUSDT(344d), COAIUSDT(344d), IRYSUSDT(330d), NIGHTUSDT(316d), RAVEUSDT(316d), XAUUSDT(315d), CYSUSDT(314d), USUSDT(314d), GUAUSDT(305d), XAGUSDT(288d), CRCLUSDT(259d), MSTRUSDT(255d), AIAUSDT(227d), BSBUSDT(211d), CLUSDT(204d), OPENAIUSDT(149d), SLXUSDT(143d), BTWUSDT(140d), CAPUSDT(117d)