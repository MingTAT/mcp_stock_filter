import tushare as ts
import pandas as pd

class SimulatorAgent:
    def __init__(self, ts_token):
        self.pro = ts.pro_api(ts_token)

    def run(self, params):
        stocks = params.get("stocks", [])
        start_date = params["start_date"]
        end_date = params["end_date"]
        principal = params["principal"]
        frequency = params["frequency"]
        shares_per_period = params["shares_per_period"]

        results = {}

        for code in stocks:
            df = self.pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
            if df.empty:
                continue
            df = df.sort_values(by="trade_date").reset_index(drop=True)

            stock_result = {}

            stock_result["lump_sum"] = self.lump_sum(df.copy(), principal)
            stock_result["fixed_amount_dca"] = self.fixed_amount_dca(df.copy(), principal, frequency)
            stock_result["fixed_shares_dca"] = self.fixed_shares_dca(df.copy(), principal, frequency, shares_per_period)

            results[code] = stock_result

        return results

    def lump_sum(self, df, principal):
        first_price = df.iloc[0]["close"]
        shares = principal / first_price
        df["total_value"] = shares * df["close"]
        df["total_invested"] = principal
        df["net_value"] = df["total_value"] / df["total_invested"]
        return {"summary": self._summary(df, principal, shares), "curve": df[["trade_date", "net_value"]]}

    def fixed_amount_dca(self, df, principal, frequency):
        total_invested = 0
        total_shares = 0
        num_periods = len(df) // frequency + 1
        invest_amount = principal / num_periods

        for i in range(0, len(df), frequency):
            price = df.loc[i, "close"]
            shares = invest_amount / price

            total_invested += invest_amount
            total_shares += shares

            df.loc[i:, "total_value"] = total_shares * df.loc[i:, "close"]
            df.loc[i:, "total_invested"] = total_invested
            df.loc[i:, "net_value"] = df.loc[i:, "total_value"] / total_invested

        return {"summary": self._summary(df, total_invested, total_shares), "curve": df[["trade_date", "net_value"]]}

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

            df.loc[i:, "total_value"] = total_shares * df.loc[i:, "close"]
            df.loc[i:, "total_invested"] = total_invested
            df.loc[i:, "net_value"] = df.loc[i:, "total_value"] / total_invested

        return {"summary": self._summary(df, total_invested, total_shares), "curve": df[["trade_date", "net_value"]]}

    def _summary(self, df, invested, shares):
        final_value = shares * df.iloc[-1]["close"]
        profit_rate = (final_value - invested) / invested * 100

        return {
            "total_invested": round(invested, 2),
            "final_value": round(final_value, 2),
            "profit_rate": round(profit_rate, 2),
            "total_shares": round(shares, 2),
        }
