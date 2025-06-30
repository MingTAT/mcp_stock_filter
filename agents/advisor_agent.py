class AdvisorAgent:
    def run(self, sim_results):
        reports = {}

        for code, strategy_results in sim_results.items():
            best_strategy = None
            best_profit = float('-inf')

            summary_lines = []

            for strat_key, result in strategy_results.items():
                profit = result["summary"]["profit_rate"]
                if profit > best_profit:
                    best_profit = profit
                    best_strategy = strat_key

                label = self._translate_label(strat_key)
                line = f"{label}: Profit Rate {profit:.2f}%, Invested {result['summary']['total_invested']}, Final Value {result['summary']['final_value']}"
                summary_lines.append(line)

            report_text = f"📄 Report for {code}\n"
            report_text += "\n".join(summary_lines)
            report_text += f"\n\n✅ Recommended Strategy: {self._translate_label(best_strategy)} with highest profit rate of {best_profit:.2f}%.\n"
            report_text += "-" * 50

            reports[code] = report_text

        # 将每个股票的报告写入一个txt文件
        with open("outputs/advisor_reports.txt", "w", encoding="utf-8") as f:
            for text in reports.values():
                f.write(text + "\n\n")

        print("✅ AI 报告已生成 outputs/advisor_reports.txt")
        return reports

    def _translate_label(self, key):
        mapping = {
            "lump_sum": "Lump Sum",
            "fixed_amount_dca": "Fixed Amount DCA",
            "fixed_shares_dca": "Fixed Shares DCA"
        }
        return mapping.get(key, key)
