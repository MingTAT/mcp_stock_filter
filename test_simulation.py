import yaml
from agents.simulator_agent import SimulatorAgent
from agents.visualizer_agent import VisualizerAgent

if __name__ == "__main__":
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    ts_token = config["tushare_token"]
    sim_params = config["simulator_params"]

    # 举例从之前 FilterAgent 输出中选股票
    # 这里直接写一个测试股票列表，例如：
    final_stocks = ["000001.SZ", "000002.SZ"]

    sim_params["stocks"] = final_stocks

    simulator_agent = SimulatorAgent(ts_token)
    sim_results = simulator_agent.run(sim_params)

    visualizer_agent = VisualizerAgent()
    visualizer_agent.run(sim_results)

    print("🎉 模拟 & 可视化完成")
