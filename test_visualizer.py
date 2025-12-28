from data_fetcher import DataFetcher
from technical_indicators import TechnicalIndicators
from visualizer import Visualizer

# 初始化模块
fetcher = DataFetcher()
ti_calculator = TechnicalIndicators()
visualizer = Visualizer()

# 获取股票数据
df = fetcher.fetch_stock_data('600000', '2023-01-01', '2023-12-31')

if df is not None:
    # 计算技术指标
    df = ti_calculator.calculate_all_indicators(df)
    
    print("\n=== 测试可视化模块 ===")
    
    # 测试K线图与均线
    try:
        fig = visualizer.plot_kline_with_ma(df)
        print("✓ K线图与均线绘制成功")
    except Exception as e:
        print(f"✗ K线图与均线绘制失败: {e}")
    
    # 测试MACD指标
    try:
        fig = visualizer.plot_macd(df)
        print("✓ MACD指标绘制成功")
    except Exception as e:
        print(f"✗ MACD指标绘制失败: {e}")
    
    # 测试RSI指标
    try:
        fig = visualizer.plot_rsi(df)
        print("✓ RSI指标绘制成功")
    except Exception as e:
        print(f"✗ RSI指标绘制失败: {e}")
    
    # 测试布林带指标
    try:
        fig = visualizer.plot_boll(df)
        print("✓ 布林带指标绘制成功")
    except Exception as e:
        print(f"✗ 布林带指标绘制失败: {e}")
    
    # 测试成交量与OBV
    try:
        fig = visualizer.plot_volume_obv(df)
        print("✓ 成交量与OBV绘制成功")
    except Exception as e:
        print(f"✗ 成交量与OBV绘制失败: {e}")
    
    # 测试组合图表
    try:
        fig = visualizer.plot_combined_charts(df)
        print("✓ 组合图表绘制成功")
    except Exception as e:
        print(f"✗ 组合图表绘制失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== 可视化模块测试完成 ===")
else:
    print("获取数据失败")