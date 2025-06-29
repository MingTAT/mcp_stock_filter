# 📊 MCP-Stock-Filter

一个基于 MCP（Model Context Protocol，模型上下文协议）设计思想构建的股票智能筛选与策略模拟小项目，使用 Tushare 数据接口，支持多阶段筛选、多策略模拟、可视化对比。该项目为后续 AI 投资 Agent 系统的起点，具备 Agent 调度、任务上下文、模块封装、结果传递等能力。

---

## 🚀 项目亮点

- ✅ MCP 架构雏形：通过 `TaskContext` 和 `Dispatcher` 管理任务与 Agent 调用
- ✅ 多阶段股票筛选：集成「天量股票检测 → 均线过滤 → 财务指标过滤」三阶段筛选逻辑
- ✅ 策略模拟 Agent：一次性买入、等额定投、固定股数定投三种策略自动对比
- ✅ 可视化 Agent：自动生成策略对比柱状图，后续可扩展净值曲线、分布图
- ✅ 完全模块化设计：可扩展更多投资策略、可视化、报告生成等

---

## 🏗️ 项目结构

```
mcp_stock_filter/
├── mcp/                      # MCP 核心
│   ├── context.py            # 任务上下文封装
│   └── dispatcher.py         # Agent 调度器
│
├── agents/                   # Agent 模块
│   ├── filter_agent.py       # 股票多阶段筛选 Agent
│   ├── simulator_agent.py    # 策略模拟 Agent
│   └── visualizer_agent.py   # 可视化 Agent
│
├── config/
│   └── config.yaml           # 配置文件（包括 Tushare Token、参数）
│
├── outputs/                  # 输出结果（图表、表格）
│
├── test_filter.py            # 测试 FilterAgent
├── test_simulation.py        # 测试 SimulatorAgent + VisualizerAgent
├── run.py                    # 总流程（可后续集成）
├── requirements.txt          # 依赖列表
├── .gitignore                # Git 忽略文件
└── README.md                 # 本文件
```

---

## 🧩 安装指南

### 1️⃣ 克隆项目

```bash
git clone https://github.com/yourusername/mcp_stock_filter.git
cd mcp_stock_filter
```

### 2️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

### 3️⃣ 配置 Tushare Token

编辑 `config/config.yaml` 文件，填入 Tushare Token，并配置筛选与模拟参数：

```yaml
tushare_token: "your_tushare_token_here"

filter_params:
  tianliang_start: "20240621"
  tianliang_end: "20250621"
  ma_list: [60, 120, 250, 610, 850, 985]
  min_profit: 0
  min_pb: 0
  max_pb: 3
  max_annual_growth: 50

simulator_params:
  start_date: "20210101"
  end_date: "20240628"
  principal: 300000
  frequency: 20
  shares_per_period: 1000
```

---

## 🛠️ 使用说明

### 运行测试

#### 测试股票筛选

```bash
python test_filter.py
```

#### 测试策略模拟 + 可视化

```bash
python test_simulation.py
```

### 输出结果

- 筛选结果保存到控制台或可写入 Excel 文件（可自行修改）
- 策略模拟结果保存为字典结构，供后续可视化使用
- 策略对比图保存在 `outputs/` 文件夹

---

## 📡 模块功能文档

### `TaskContext`

```python
TaskContext(task_type: str, params: dict)
```

- 存储任务类型、参数、结果。

### `Dispatcher`

```python
Dispatcher.register_agent(task_type: str, agent: object)
Dispatcher.run(context: TaskContext) -> TaskContext
```

- 注册并调度 Agent。

### `FilterAgent`

```python
FilterAgent(ts_token: str).run(params: dict) -> list
```

- 综合多阶段筛选，返回最终股票列表。

### `SimulatorAgent`

```python
SimulatorAgent(ts_token: str).run(params: dict) -> dict
```

- 对输入股票列表执行多策略模拟，返回各策略表现结果。

### `VisualizerAgent`

```python
VisualizerAgent().run(sim_results: dict)
```

- 将模拟结果生成对比图。

---

## 🧱 示例结果截图

> 策略模拟示例对比图（已生成 outputs 文件夹）：

```
000001.SZ_strategy_comparison.png
```

---

## 📌 后续规划

| 功能             | 描述                          |
|----------------|-----------------------------|
| 📈 净值曲线绘制  | 每个策略的净值随时间变化趋势图 |
| 🧾 Excel 导出  | 各策略详细模拟结果表格导出   |
| 🤖 Advisor Agent | 自动生成多策略比较的自然语言报告 |
| 🔄 MCP 完整流程 | 多 Agent 串联，支持自动交互   |

---

## 📜 License

本项目采用 MIT License，欢迎 Fork、贡献 PR 或提出建议。

---

## 🙋‍♀️ 作者

Made with ❤ by MingTAT  
喜欢的话，欢迎 Star ⭐、Fork 🍴 或提出 issue 一起完善！🔥
