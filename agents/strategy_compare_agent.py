import tushare as ts
import pandas as pd

class StrategyCompareAgent:
    def __init__(self, ts_token):
        self.pro = ts.pro_api(ts_token)

        # 策略注册表
        self.strategies = {
            "lump_sum": self.lump_sum,
            "fixed_amount_dca": self.fixed_amount_dca,
            "fixed_shares_dca": self.fixed_shares_dca,
        }

    def run(self, params):
        ts_code = params.get("ts_code")
        start_date = params.get("start_date")
        end_date = params.get("end_date")
        principal = params.get("principal", 300000)
        frequency = params.get("frequency", 20)
        shares_per_period = params.get("shares_per_period", 1000)  # 仅用于固定股数定投

        if not ts_code or not start_date or not end_date:
            print("⚠️ 缺少必要参数 ts_code/start_date/end_date")
            return None

        # 获取历史行情
        df = self.pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        if df.empty:
            print("⚠️ 未获取到行情数据")
            return None

        df = df.sort_values(by="trade_date").reset_index(drop=True)

        # 调用每个策略，收集结果
        results = {}
        for strategy_name, strategy_func in self.strategies.items():
            result = strategy_func(df.copy(), principal, frequency, shares_per_period)
            results[strategy_name] = result

        return results

    def lump_sum(self, df, principal, frequency, shares_per_period):
        first_price = df.loc[0, "close"]
        shares = principal / first_price
        final_value = shares * df.loc[len(df) - 1, "close"]
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

        final_value = total_shares * df.loc[len(df) - 1, "close"]
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
                break  # 超出本金，停止买入

            total_invested += invest_amount
            total_shares += shares_per_period

        final_value = total_shares * df.loc[len(df) - 1, "close"]
        profit_rate = (final_value - total_invested) / total_invested * 100

        return {
            "strategy": "固定股数定投",
            "total_invested": round(total_invested, 2),
            "final_value": round(final_value, 2),
            "profit_rate": round(profit_rate, 2),
            "total_shares": round(total_shares, 2),
        }
