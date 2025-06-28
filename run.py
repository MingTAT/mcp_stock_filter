import yaml
from mcp.context import TaskContext
from mcp.dispatcher import Dispatcher
from agents.filter_agent import FilterAgent

if __name__ == "__main__":
    # 读取配置
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    ts_token = config["tushare_token"]

    # 初始化 Agent
    filter_agent = FilterAgent(ts_token)

    # 初始化 MCP 调度器
    dispatcher = Dispatcher()
    dispatcher.register_agent("stock_filter", filter_agent)

    # 模拟用户输入参数
    params = {
        "market": "主板",       # 示例：只看主板
        "industry": ""         # 示例：可填某个行业，比如"酿酒"
    }

    context = TaskContext(task_type="stock_filter", params=params)

    # 调用 Agent
    context = dispatcher.run(context)

    df = context.results.get("stock_filter")

    if df is not None:
        print(df.head())
        # 保存结果，可选
        df.to_excel("outputs/stock_filter_results.xlsx", index=False)
        print("✅ 筛选结果已保存到 outputs/stock_filter_results.xlsx")
    else:
        print("⚠️ 没有返回结果")
