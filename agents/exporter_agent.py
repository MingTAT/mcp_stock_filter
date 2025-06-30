import pandas as pd

class ExporterAgent:
    def run(self, sim_results):
        writer = pd.ExcelWriter("outputs/strategy_results.xlsx", engine="openpyxl")

        for code, strategy_results in sim_results.items():
            all_strategies_df = []

            for strat_key, result in strategy_results.items():
                curve = result["curve"].copy()
                curve = curve.rename(columns={"net_value": f"{strat_key}_net_value"})
                curve[f"{strat_key}_total_invested"] = result["summary"]["total_invested"]
                curve[f"{strat_key}_final_value"] = result["summary"]["final_value"]
                curve[f"{strat_key}_profit_rate"] = result["summary"]["profit_rate"]

                curve["strategy"] = strat_key
                all_strategies_df.append(curve)

            # 合并所有策略
            full_df = pd.concat(all_strategies_df, ignore_index=True)
            full_df = full_df.sort_values(by=["strategy", "trade_date"])

            # 写入 Excel sheet
            sheet_name = code.replace(".", "_")
            full_df.to_excel(writer, sheet_name=sheet_name, index=False)

        writer.close()
        print("✅ Excel 文件已生成 outputs/strategy_results.xlsx")
