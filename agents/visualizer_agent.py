import matplotlib.pyplot as plt

class VisualizerAgent:
    def run(self, sim_results):
        for code, strategy_results in sim_results.items():
            # 策略收益率对比柱状图
            strategies = []
            profits = []

            for strat_key, result in strategy_results.items():
                label = self._translate_label(strat_key)
                strategies.append(label)
                profits.append(result["summary"]["profit_rate"])

            plt.figure(figsize=(8, 5))
            plt.bar(strategies, profits, color='skyblue')
            plt.title(f"{code} Strategy Profit Comparison")
            plt.ylabel("Profit Rate (%)")
            plt.savefig(f"outputs/{code}_strategy_comparison.png")
            plt.close()

            # 净值曲线图
            plt.figure(figsize=(10, 6))
            for strat_key, result in strategy_results.items():
                curve = result["curve"]
                label = self._translate_label(strat_key)
                plt.plot(curve["trade_date"], curve["net_value"], label=label)

            plt.title(f"{code} Strategy Net Value Curve")
            plt.xlabel("Date")
            plt.ylabel("Net Value (Relative to Invested)")
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.savefig(f"outputs/{code}_net_value_curve.png")
            plt.close()

        print("✅ Strategy comparison and net value curves have been generated in outputs/")

    def _translate_label(self, key):
        mapping = {
            "lump_sum": "Lump Sum",
            "fixed_amount_dca": "Fixed Amount DCA",
            "fixed_shares_dca": "Fixed Shares DCA"
        }
        return mapping.get(key, key)
