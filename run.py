import yaml
from mcp.context import TaskContext
from mcp.dispatcher import Dispatcher
from agents.filter_agent import FilterAgent
from agents.simulator_agent import SimulatorAgent
from agents.strategy_compare_agent import StrategyCompareAgent

if __name__ == "__main__":
    # 加载配置
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    ts_token = config["tushare_token"]

    # 初始化 Agents
    filter_agent = FilterAgent(ts_token)
    simulator_agent = SimulatorAgent(ts_token)
    strategy_agent = StrategyCompareAgent(ts_token)

    # 注册到 Dispatcher
    dispatcher = Dispatcher()
    dispatcher.register_agent("stock_filter", filter_agent)
    dispatcher.register_agent("simulate_dingtou", simulator_agent)
    dispatcher.register_agent("strategy_compare", strategy_agent)

    # 举例完整流程执行一次
    params = config["filter_params"]

    context = TaskContext(task_type="stock_filter", params=params)
    context = dispatcher.run(context)
    df = context.results.get("stock_filter")

    if df is not None:
        print(df.head())
        df.to_excel("outputs/filter_results.xlsx", index=False)
        print("✅ 筛选结果已保存")
    else:
        print("⚠️ 没有筛选结果")
