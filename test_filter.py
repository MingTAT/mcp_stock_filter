import yaml
from agents.filter_agent import FilterAgent

if __name__ == "__main__":
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    ts_token = config["tushare_token"]
    params = config["filter_params"]

    agent = FilterAgent(ts_token)
    df = agent.run(params)

    if df is not None:
        print(df.head())
        df.to_excel("outputs/filter_test.xlsx", index=False)
        print("✅ 筛选测试结果已保存")
    else:
        print("⚠️ 没有结果")
