import tushare as ts
import pandas as pd
from tqdm import tqdm

class SimulatorAgent:
    def __init__(self, ts_token):
        self.pro = ts.pro_api(ts_token)

        self.strategies = {
            "lump_sum": self.lump_sum,
            "fixed_amount_dca": self.fixed_amount_dca,
            "fixed_shares_dca": self.fixed_shares_dca,
        }

    def run(self, params):
        stocks = params.get("stocks", [])
        start_date = params["start_date"]
        end_date = params["end_date"]
        principal = params["principal"]
        frequency = params["frequency"]
        shares_per_period = params["shares_per_period"]

        results = {}

        for code in tqdm(stocks, desc="策略模拟"):
            try:
                df = self.pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
                if df.empty:
                    continue
                df = df.sort_values(by="trade_date").reset_index(drop=True)

                stock_result = {}
                for strategy_name, func in self.strategies.items():
                    result = func(df.copy(), principal, frequency, shares_per_period)
                    stock_result[strategy_name] = result

                results[code] = stock_result
            except Exception as e:
                print(f"⚠️ 股票 {code} 出错：{e}")
                continue

        return results

    def lump_sum(self, df, principal, frequency, shares_per_period):
        first_price = df.iloc[0]["close"]
        shares = principal / first_price
        final_price = df.iloc[-1]["close"]
        final_value = shares * final_price
        profit_rate = (final_value - principal) / principal * 100

        return {
            "strategy": "一次性买入",
            "total_invested": round(principal, 2),
            "final_value": round(final_value, 2),
            "profit_rate": round(profit_rate, 2),
            "total_shares": round(shares, 2),
        }

    def fixed_amount_dca(self, df, principal, frequency, shares_per_period):
        total_invested = 0
        total_shares = 0
        num_periods = len(df) // frequency + 1
        invest_amount = principal / num_periods

        for i in range(0, len(df), frequency):
            price = df.loc[i, "close"]
            shares = invest_amount / price

            total_invested += invest_amount
            total_shares += shares

        final_value = total_shares * df.iloc[-1]["close"]
        profit_rate = (final_value - total_invested) / total_invested * 100

        return {
            "strategy": "等额定投",
            "total_invested": round(total_invested, 2),
            "final_value": round(final_value, 2),
            "profit_rate": round(profit_rate, 2),
            "total_shares": round(total_shares, 2),
        }

    def fixed_shares_dca(self, df, principal, frequency, shares_per_period):
        total_invested = 0
        total_shares = 0

        for i in range(0, len(df), frequency):
            price = df.loc[i, "close"]
            invest_amount = shares_per_period * price

            if total_invested + invest_amount > principal:
                break

            total_invested += invest_amount
            total_shares += shares_per_period

        final_value = total_shares * df.iloc[-1]["close"]
        profit_rate = (final_value - total_invested) / total_invested * 100

        return {
            "strategy": "固定股数定投",
            "total_invested": round(total_invested, 2),
            "final_value": round(final_value, 2),
            "profit_rate": round(profit_rate, 2),
            "total_shares": round(total_shares, 2),
        }
