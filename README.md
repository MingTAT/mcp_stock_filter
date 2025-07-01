# 📊 MCP-Stock-Filter

一个基于 MCP（Model Context Protocol，模型上下文协议）设计思想构建的股票智能筛选与多策略模拟项目，使用 Tushare 数据接口，支持多阶段筛选、策略模拟、可视化、Excel 导出及自动生成 AI 报告。  
该项目为后续 AI 投资 Agent 系统的基础雏形，支持任务上下文管理、模块化封装、风险指标分析等功能。

---

## 🚀 项目亮点

- ✅ MCP 架构：通过 `TaskContext` + `Dispatcher` 串联多 Agent
- ✅ 多阶段股票筛选：天量成交检测、均线过滤、财务指标过滤
- ✅ 策略模拟：一次性买入、等额定投、固定股数定投
- ✅ 风险指标分析：最大回撤、夏普比率
- ✅ 可视化图表：收益柱状图、净值曲线图
- ✅ Excel 导出：详细策略数据
- ✅ AI 报告生成：自然语言总结，自动生成 txt 报告

---

## 🏗️ 项目结构

```
mcp_stock_filter/
├── mcp/
│   ├── context.py
│   └── dispatcher.py
│
├── agents/
│   ├── filter_agent.py
│   ├── simulator_agent.py
│   ├── visualizer_agent.py
│   ├── exporter_agent.py
│   ├── advisor_agent.py
│   └── strategy_compare_agent.py （可选）
│
├── config/
│   └── config.yaml
│
├── outputs/                      # 生成图表、Excel、报告
├── run.py                        # 一键总流程
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

流程包含：

1️⃣ 股票筛选（FilterAgent）  
2️⃣ 策略模拟（SimulatorAgent）  
3️⃣ 风险指标分析（最大回撤、夏普比率）  
4️⃣ 图表生成（VisualizerAgent）  
5️⃣ Excel 导出（ExporterAgent）  
6️⃣ AI 报告生成（AdvisorAgent）

所有结果保存在 `outputs/` 文件夹。

---

## 📡 Agent 模块说明

### `TaskContext`

任务上下文，存储任务类型、参数、结果。

### `Dispatcher`

注册并调度 Agent，可串联多个 Agent 任务。

### `FilterAgent`

多阶段股票筛选逻辑。

### `SimulatorAgent`

三种策略模拟，附带净值曲线、风险指标（最大回撤、夏普比率）。

### `VisualizerAgent`

生成柱状收益对比图、净值曲线图。

### `ExporterAgent`

详细导出策略结果 Excel 文件。

### `AdvisorAgent`

自动生成自然语言总结报告，输出 `advisor_reports.txt`。

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

| 功能            | 描述                            |
|---------------|-------------------------------|
| 📈 年化波动率分析 | 更全面的风险衡量              |
| 🧾 GPT 报告生成 | 使用 LLM 自动生成完整报告  |
| 💬 CLI 交互封装 | 交互式配置股票池与参数    |
| 🌐 前端界面    | Streamlit/Gradio 快速预览 |

---

## 📜 License

MIT License，欢迎 Fork、PR 或提出建议 🙌

---

## 🙋‍♀️ 作者

Made with ❤ by MingTAT  
喜欢的话，欢迎 Star ⭐、Fork 🍴、或者提 issue 一起完善！🔥
