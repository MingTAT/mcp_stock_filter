# 📊 MCP-Stock-Filter

一个基于 MCP（Model Context Protocol，模型上下文协议）设计思想构建的股票智能筛选与多策略模拟项目，使用 Tushare 数据接口，支持多阶段筛选、策略模拟、可视化对比、Excel 导出及自动生成报告。  
该项目为后续 AI 投资 Agent 系统的基础雏形，支持 Agent 调度、任务上下文、模块化封装与结果自动生成。

---

## 🚀 项目亮点

- ✅ MCP 架构：通过 `TaskContext` 和 `Dispatcher` 串联多 Agent
- ✅ 多阶段股票筛选：集成「天量成交检测 → 均线过滤 → 财务指标过滤」
- ✅ 策略模拟 Agent：一次性买入、等额定投、固定股数定投三种策略
- ✅ 可视化 Agent：柱状对比图 + 净值曲线图自动生成
- ✅ Excel 导出 Agent：生成详细策略结果表格
- ✅ AI 报告 Agent：自动生成自然语言总结报告

---

## 🏗️ 项目结构

```
mcp_stock_filter/
├── mcp/
│   ├── context.py
│   └── dispatcher.py
│
├── agents/
│   ├── filter_agent.py           # 股票筛选
│   ├── simulator_agent.py        # 策略模拟
│   ├── visualizer_agent.py       # 图表生成
│   ├── exporter_agent.py         # Excel 导出 ✅
│   ├── advisor_agent.py          # AI 报告 ✅
│   └── strategy_compare_agent.py 
│
├── config/
│   └── config.yaml
│
├── outputs/                      # 生成图表、Excel、报告
├── run.py                        # 一键总流程 ✅
├── test_filter.py
├── test_simulation.py
├── README.md
├── requirements.txt
└── .gitignore
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

编辑 `config/config.yaml` 文件：

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

### 🔥 一键全流程运行

```bash
python run.py
```

该命令会自动完成以下步骤：

1️⃣ 股票筛选（FilterAgent）  
2️⃣ 策略模拟（SimulatorAgent）  
3️⃣ 图表生成（VisualizerAgent）  
4️⃣ Excel 导出（ExporterAgent）  
5️⃣ AI 报告生成（AdvisorAgent）  

所有结果会保存到 `outputs/` 文件夹。

---

## 📡 Agent 模块说明

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
- 注册并调度 Agent，支持多 Agent 串联执行。

### `FilterAgent`

多阶段筛选，输出股票列表。

### `SimulatorAgent`

多策略模拟，返回详细收益曲线与汇总。

### `VisualizerAgent`

生成柱状收益对比图 & 净值曲线图。

### `ExporterAgent`

将详细策略结果导出 Excel 文件（`outputs/strategy_results.xlsx`）。

### `AdvisorAgent`

自动生成策略总结报告（`outputs/advisor_reports.txt`）。

---

## 📄 输出文件

```
outputs/
├── 000001.SZ_strategy_comparison.png
├── 000001.SZ_net_value_curve.png
├── strategy_results.xlsx
├── advisor_reports.txt
```

---

## 📌 后续规划

| 功能            | 描述                              |
|---------------|---------------------------------|
| 📈 风险指标分析 | 最大回撤、夏普比率等             |
| 🧾 高级报告生成 | 结合 GPT 自动化完整文字报告        |
| 💬 CLI 交互封装 | 允许命令行配置参数、选股票       |
| 🌐 Web 前端    | Streamlit/Gradio 快速原型     |

---

## 📜 License

本项目采用 MIT License，欢迎 Fork、PR 或提出建议 🙌

---

## 🙋‍♀️ 作者

Made with ❤ by MingTAT  
喜欢的话，欢迎 Star ⭐、Fork 🍴 或提出 issue 一起完善！🔥
