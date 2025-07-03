import yaml
from mcp.context import TaskContext
from mcp.dispatcher import Dispatcher
from agents.filter_agent import FilterAgent
from agents.simulator_agent import SimulatorAgent
from agents.visualizer_agent import VisualizerAgent
from agents.exporter_agent import ExporterAgent
from agents.advisor_agent import AdvisorAgent
from agents.advanced_strategy_agent import AdvancedStrategyAgent

if __name__ == "__main__":
    # 读取配置
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    ts_token = config["tushare_token"]
    filter_params = config["filter_params"]
    simulator_params = config["simulator_params"]

    # 初始化 Agent
    filter_agent = FilterAgent(ts_token)
    simulator_agent = SimulatorAgent(ts_token)
    visualizer_agent = VisualizerAgent()
    exporter_agent = ExporterAgent()
    advisor_agent = AdvisorAgent()

    # 初始化 MCP Dispatcher
    dispatcher = Dispatcher()
    dispatcher.register_agent("filter", filter_agent)
    dispatcher.register_agent("simulate", simulator_agent)
    dispatcher.register_agent("visualize", visualizer_agent)
    dispatcher.register_agent("export", exporter_agent)
    dispatcher.register_agent("advisor", advisor_agent)

    # ========== Step 1: 股票筛选 ==========
    filter_context = TaskContext(task_type="filter", params=filter_params)
    filter_context = dispatcher.run(filter_context)
    final_stocks = filter_context.results.get("filter")

    if not final_stocks:
        print("⚠️ 没有筛选到股票，流程结束")
        exit()

    print(f"✅ 筛选完成，共 {len(final_stocks)} 只股票，将进入模拟")

    # ========== Step 2: 策略模拟 ==========
    sim_params = simulator_params.copy()
    sim_params["stocks"] = final_stocks

    simulate_context = TaskContext(task_type="simulate", params=sim_params)
    simulate_context = dispatcher.run(simulate_context)
    sim_results = simulate_context.results.get("simulate")

    if not sim_results:
        print("⚠️ 模拟无结果，流程结束")
        exit()

    print("✅ 策略模拟完成，开始生成图表")

    # ========== Step 3: 图表生成 ==========
    visualize_context = TaskContext(task_type="visualize", params={"sim_results": sim_results})
    visualize_context = dispatcher.run(visualize_context)

    # ========== Step 4: Excel 导出 ==========
    export_context = TaskContext(task_type="export", params={"sim_results": sim_results})
    export_context = dispatcher.run(export_context)

    # ========== Step 5: AI 报告生成 ==========
    advisor_context = TaskContext(task_type="advisor", params={"sim_results": sim_results})
    advisor_context = dispatcher.run(advisor_context)

    print("🎉 全流程完成，所有输出已生成 outputs 文件夹 ✅")

    for code in final_stocks:
        df = simulator_agent.pro.daily(ts_code=code, start_date=simulator_params["start_date"], end_date=simulator_params["end_date"])
        if df.empty:
            continue

    strategy_agent = AdvancedStrategyAgent(df)
    curve1 = strategy_agent.enhanced_indexing()
    curve2 = strategy_agent.momentum()
    curve3 = strategy_agent.trend_following()
    combined_curve, weights = strategy_agent.auto_weighted_composite([curve1, curve2, curve3])

    # 输出组合信息
    print(f"✅ 高级策略组合 - {code}")
    print(f"组合权重: {weights}")
