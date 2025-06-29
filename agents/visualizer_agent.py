import matplotlib.pyplot as plt

class VisualizerAgent:
    def run(self, sim_results):
        for code, strategy_results in sim_results.items():
            strategies = []
            profits = []

            for strat_name, result in strategy_results.items():
                # 转换策略名称为英文，防止中文警告
                if result["strategy"] == "一次性买入":
                    strategies.append("Lump Sum")
                elif result["strategy"] == "等额定投":
                    strategies.append("Fixed Amount DCA")
                elif result["strategy"] == "固定股数定投":
                    strategies.append("Fixed Shares DCA")
                else:
                    strategies.append(result["strategy"])

                profits.append(result["profit_rate"])

            plt.figure(figsize=(8, 5))
            plt.bar(strategies, profits, color='skyblue')
            plt.title(f"{code} Strategy Comparison")
            plt.ylabel("Profit Rate (%)")
            plt.savefig(f"outputs/{code}_strategy_comparison.png")
            plt.close()

        print("✅ Strategy comparison chart has been generated outputs/")
