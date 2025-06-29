import tushare as ts
import pandas as pd
import numpy as np
from tqdm import tqdm

class FilterAgent:
    def __init__(self, ts_token):
        self.pro = ts.pro_api(ts_token)

    def run(self, params):
        # 所有参数都从 params 读取
        start_date = params["tianliang_start"]
        end_date = params["tianliang_end"]
        ma_list = params["ma_list"]
        min_profit = params["min_profit"]
        min_pb = params["min_pb"]
        max_pb = params["max_pb"]
        max_annual_growth = params["max_annual_growth"]

        final_stock_list = []

        stock_list = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,name')

        for code in tqdm(stock_list['ts_code'].tolist(), desc="多阶段筛选"):
            try:
                # Step 1: 天量
                df_vol = self.pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
                if df_vol.empty or df_vol["vol"].max() < df_vol["vol"].quantile(0.99):
                    continue

                # Step 2: 均线
                df_ma = self.pro.daily(ts_code=code, start_date="20220101", end_date=end_date)
                if df_ma.empty or len(df_ma) < max(ma_list):
                    continue
                df_ma = df_ma.sort_values(by="trade_date").reset_index(drop=True)
                for ma in ma_list:
                    df_ma[f"ma{ma}"] = df_ma['close'].rolling(ma).mean()
                latest = df_ma.iloc[-1]
                price = latest['close']
                if not all([price > latest[f"ma{ma}"] for ma in ma_list if not np.isnan(latest[f"ma{ma}"])]):
                    continue

                # Step 3: 财务
                fin = self.pro.fina_indicator_vip(ts_code=code)
                if fin.empty or fin.iloc[-1]['netprofit_margin'] < min_profit:
                    continue
                daily_basic = self.pro.daily_basic(ts_code=code, trade_date=end_date)
                if daily_basic.empty:
                    continue
                pb = daily_basic.iloc[-1]['pb']
                if pb <= min_pb or pb >= max_pb:
                    continue
                hist = self.pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
                if hist.empty:
                    continue
                start_price = hist.iloc[0]['close']
                end_price = hist.iloc[-1]['close']
                growth = (end_price - start_price) / start_price * 100
                if growth >= max_annual_growth:
                    continue

                final_stock_list.append(code)
            except:
                continue

        print(f"✅ 最终筛选后股票数: {len(final_stock_list)}")
        return final_stock_list
