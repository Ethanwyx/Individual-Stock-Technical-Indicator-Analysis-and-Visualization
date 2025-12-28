import streamlit as st
from data_fetcher import DataFetcher
from technical_indicators import TechnicalIndicators
from visualizer import Visualizer
from datetime import datetime, timedelta
import pandas as pd

# 页面配置
st.set_page_config(
    page_title="个股技术指标分析与可视化",
    page_icon="📈",
    layout="wide"
)

# 初始化
fetcher = DataFetcher()
ti_calculator = TechnicalIndicators()
visualizer = Visualizer()

# 页面标题
st.title("📈 个股技术指标分析与可视化")

# 创建侧边栏
st.sidebar.header("参数设置")

# 股票代码输入
stock_symbol = st.sidebar.text_input("股票代码", value="600000", help="输入A股股票代码，如：600000")

# 时间范围选择
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

start_date = st.sidebar.date_input("开始日期", value=pd.to_datetime(start_date))
end_date = st.sidebar.date_input("结束日期", value=pd.to_datetime(end_date))

# 转换为字符串格式
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

# 指标选择
st.sidebar.header("指标选择")
show_ma = st.sidebar.checkbox("移动平均线(MA)", value=True)
show_macd = st.sidebar.checkbox("MACD", value=True)
show_kdj = st.sidebar.checkbox("KDJ", value=True)
show_rsi = st.sidebar.checkbox("RSI", value=True)
show_boll = st.sidebar.checkbox("布林带(BOLL)", value=True)
show_volume_obv = st.sidebar.checkbox("成交量与OBV", value=True)
show_combined = st.sidebar.checkbox("组合图表", value=True)

# 主界面内容
if st.sidebar.button("开始分析"):
    with st.spinner("正在获取数据..."):
        # 获取股票数据
        df = fetcher.fetch_stock_data(stock_symbol, start_date_str, end_date_str)
        
        if df is not None:
            st.success(f"成功获取 {stock_symbol} 股票数据")
            
            # 计算技术指标
            df = ti_calculator.calculate_all_indicators(df)
            
            # 显示数据表格
            st.subheader("📊 股票历史数据")
            st.dataframe(df.tail(20), use_container_width=True)
            
            # 显示图表
            st.subheader("📈 技术指标图表")
            
            # 显示各个指标图表
            if show_ma:
                st.markdown("### K线图与移动平均线")
                fig = visualizer.plot_kline_with_ma(df)
                st.plotly_chart(fig, use_container_width=True)
            
            if show_macd:
                st.markdown("### MACD指标")
                fig = visualizer.plot_macd(df)
                st.plotly_chart(fig, use_container_width=True)
            
            if show_kdj:
                st.markdown("### KDJ指标")
                fig = visualizer.plot_kdj(df)
                st.plotly_chart(fig, use_container_width=True)
            
            if show_rsi:
                st.markdown("### RSI指标")
                fig = visualizer.plot_rsi(df)
                st.plotly_chart(fig, use_container_width=True)
            
            if show_boll:
                st.markdown("### 布林带指标")
                fig = visualizer.plot_boll(df)
                st.plotly_chart(fig, use_container_width=True)
            
            if show_volume_obv:
                st.markdown("### 成交量与OBV指标")
                fig = visualizer.plot_volume_obv(df)
                st.plotly_chart(fig, use_container_width=True)
            
            # 显示组合图表
            if show_combined:
                st.markdown("### 组合技术指标图表")
                fig = visualizer.plot_combined_charts(df)
                st.plotly_chart(fig, use_container_width=True)
            
            # 显示统计信息
            st.subheader("📋 股票统计信息")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("最新收盘价", f"{df['close'].iloc[-1]:.2f}元")
            with col2:
                change = df['close'].iloc[-1] - df['close'].iloc[-2]
                change_pct = (change / df['close'].iloc[-2]) * 100
                st.metric("涨跌额", f"{change:.2f}元", f"{change_pct:.2f}%")
            with col3:
                st.metric("最高价", f"{df['high'].max():.2f}元")
            with col4:
                st.metric("最低价", f"{df['low'].min():.2f}元")
        else:
            st.error(f"获取 {stock_symbol} 股票数据失败，请检查股票代码和网络连接")

# 页面说明
st.sidebar.markdown("---")
st.sidebar.markdown("### 使用说明")
st.sidebar.markdown("1. 输入股票代码")
st.sidebar.markdown("2. 选择时间范围")
st.sidebar.markdown("3. 选择要查看的指标")
st.sidebar.markdown("4. 点击开始分析")
st.sidebar.markdown("5. 查看图表和数据")

# 底部信息
st.markdown("---")
st.markdown("### 关于")
st.markdown("本应用使用Python和Streamlit开发，用于个股技术指标分析与可视化。")
st.markdown("数据来源：akshare")
st.markdown("技术指标计算：talib")
st.markdown("图表绘制：plotly")