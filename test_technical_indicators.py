from data_fetcher import DataFetcher
from technical_indicators import TechnicalIndicators

# 初始化模块
fetcher = DataFetcher()
ti_calculator = TechnicalIndicators()

# 获取股票数据
df = fetcher.fetch_stock_data('600000', '2023-01-01', '2023-12-31')

if df is not None:
    print("\n=== 原始数据 ===")
    print(df.head())
    
    # 计算技术指标
    df = ti_calculator.calculate_all_indicators(df)
    
    print("\n=== 计算技术指标后 ===")
    print(df.columns.tolist())
    print(df.tail())
else:
    print("获取数据失败")