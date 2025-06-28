# 📊 MCP-Stock-Filter

一个基于 MCP（Model Context Protocol，模型上下文协议）设计思想构建的股票筛选小项目，使用 Tushare 数据接口，支持多条件筛选与模块化扩展。该项目旨在作为后续 AI 投资 Agent 系统的起点，实现 Agent 任务调度、结果封装、统一上下文管理等功能。

---

## 🚀 项目亮点

- ✅ MCP 架构雏形：使用 `TaskContext` 和 `Dispatcher` 模拟最小调度系统
- ✅ 股票筛选 Agent：支持按市场、行业等筛选股票清单
- ✅ 可扩展设计：未来可接入定投模拟、策略对比、AI 投资建议等 Agent
- ✅ 数据实时来源：调用 Tushare Pro 接口，数据可靠，支持 A 股市场

---

## 🏗️ 项目结构

```
mcp_stock_filter/
├── mcp/                    # MCP协议核心
│   ├── context.py          # 任务上下文封装
│   └── dispatcher.py       # Agent 调度管理器
│
├── agents/                 # 业务 Agent 模块
│   └── filter_agent.py     # 股票筛选 Agent
│
├── config/
│   └── config.yaml         # Tushare token 配置文件（已 .gitignore）
│
├── data/                   # 数据缓存目录（可选）
├── outputs/                # 结果输出目录（如筛选结果 Excel）
│
├── run.py                  # 主程序入口
├── requirements.txt        # 项目依赖列表
├── .gitignore              # 忽略不应上传的文件
└── README.md               # 项目说明文档（本文件）
```

---

## 🧩 安装指南

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/mcp_stock_filter.git
cd mcp_stock_filter
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 Tushare Token

编辑 `config/config.yaml` 文件，填入你在 Tushare 官网获取的 Token：

```yaml
tushare_token: "your_tushare_token_here"
```

---

## 🛠️ 使用说明

### 运行主程序

```bash
python run.py
```

### 示例筛选条件

在 `run.py` 中可自定义参数：

```python
params = {
    "market": "主板",     # 市场类型（如 主板、创业板、中小板）
    "industry": ""        # 行业筛选（如 "酿酒行业"，留空为全部）
}
```

### 输出说明

- 控制台将输出筛选结果前几行；
- 筛选结果自动保存在 `outputs/stock_filter_results.xlsx` 文件中。

---

## 📡 API 文档

### `TaskContext`

```python
TaskContext(task_type: str, params: dict)
```

- 封装任务类型与输入参数，并存储各 Agent 执行结果。

### `Dispatcher`

```python
Dispatcher.register_agent(task_type: str, agent: object)
Dispatcher.run(context: TaskContext) -> TaskContext
```

- 注册 Agent 到调度器；
- 根据上下文任务类型自动调用对应 Agent 并返回结果。

### `FilterAgent`

```python
FilterAgent(ts_token: str).run(params: dict) -> pd.DataFrame
```

- 支持按市场、行业字段筛选上市公司基础信息；
- 返回 DataFrame 结构数据，支持保存或后续处理。

---

## 🧱 示例结果截图

> 筛选“主板市场”股票示例（结果前几行）：

| ts_code     | name | area | industry | market |
|-------------|------|------|----------|--------|
| 000001.SZ   | 平安银行 | 深圳 | 银行 | 主板 |
| 000002.SZ   | 万科A | 深圳 | 地产 | 主板 |
| ...         | ...  | ...  | ...      | ...    |

---

## 📌 后续规划

| 功能 | 描述 |
|------|------|
| 🧠 定投模拟 Agent | 输入起始金额、组合方案，模拟定投收益表现 |
| 📈 策略对比 Agent | 多种投资策略回测对比，输出风险收益比 |
| 🤖 Advisor Agent | 基于用户目标 + 数据，GPT 生成自然语言投资建议 |
| 🔄 MCP 扩展 | 支持多 Agent 协同、结果流转、权限上下文等 |

---

## 📜 License

本项目采用 MIT License 开源协议，欢迎 fork 和二次开发。

---

## 🙋‍♀️ 作者

Made with 💻 by [YourName]  
如果你喜欢这个项目，欢迎 Star ⭐、Fork 🍴 或提出建议 🙌
