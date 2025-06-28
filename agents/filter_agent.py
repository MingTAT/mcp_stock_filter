import tushare as ts
import pandas as pd

class FilterAgent:
    def __init__(self, ts_token):
        self.pro = ts.pro_api(ts_token)

    def run(self, params):
        # 示例：只用基本信息，后续可根据params增加筛选条件
        df = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,market,list_date')
        
        # 可以根据 params 自定义筛选，如筛选上市时间、市场、行业等
        if 'market' in params and params['market']:
            df = df[df['market'] == params['market']]
        
        if 'industry' in params and params['industry']:
            df = df[df['industry'] == params['industry']]

        df = df.reset_index(drop=True)
        return df
