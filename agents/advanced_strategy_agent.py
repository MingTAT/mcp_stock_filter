import pandas as pd
import numpy as np

class AdvancedStrategyAgent:
    def __init__(self, df):
        self.df = df.copy()
        self.df = self.df.sort_values(by="trade_date").reset_index(drop=True)

    def enhanced_indexing(self, alpha=0.02):
        # 模拟指数增强：每日多获得一个小 alpha 收益
        base_return = self.df["close"].pct_change().fillna(0)
        extra_alpha = alpha / len(self.df)
        enhanced_return = base_return + extra_alpha
        curve = (1 + enhanced_return).cumprod()
        return curve

    def momentum(self, window=20):
        self.df["momentum"] = self.df["close"].pct_change(periods=window).fillna(0)
        signal = self.df["momentum"] > 0
        daily_return = self.df["close"].pct_change().fillna(0)
        strat_return = daily_return * signal
        curve = (1 + strat_return).cumprod()
        return curve

    def trend_following(self, ma_window=60):
        self.df["ma"] = self.df["close"].rolling(ma_window).mean()
        signal = self.df["close"] > self.df["ma"]
        daily_return = self.df["close"].pct_change().fillna(0)
        strat_return = daily_return * signal
        curve = (1 + strat_return).cumprod()
        return curve

    def auto_weighted_composite(self, curves):
        final_values = [c.iloc[-1] for c in curves]
        total = sum(final_values)
        weights = [v / total for v in final_values]
        combined_curve = sum(w * c for w, c in zip(weights, curves))
        return combined_curve, weights
