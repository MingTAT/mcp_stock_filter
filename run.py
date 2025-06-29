import yaml
from mcp.context import TaskContext
from mcp.dispatcher import Dispatcher
from agents.filter_agent import FilterAgent
from agents.simulator_agent import SimulatorAgent
from agents.visualizer_agent import VisualizerAgent

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

    # 注册 MCP Dispatcher
    dispatcher = Dispatcher()
    dispatcher.register_agent("filter", filter_agent)
    dispatcher.register_agent("simulate", simulator_agent)
    dispatcher.register_agent("visualize", visualizer_agent)

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

    # ========== Step 3: 可视化 ==========
    visualize_context = TaskContext(task_type="visualize", params={"sim_results": sim_results})
    visualize_context = dispatcher.run(visualize_context)

    print("🎉 全流程完成，图表已生成 outputs 文件夹")
