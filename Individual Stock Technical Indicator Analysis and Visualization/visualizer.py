import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class Visualizer:
    def __init__(self):
        pass
    
    def plot_kline_with_ma(self, df, ma_periods=[5, 10, 20, 60]):
        """
        绘制K线图并叠加移动平均线
        
        参数:
            df: 包含股票数据和均线的DataFrame
            ma_periods: 要显示的均线周期列表
        
        返回:
            go.Figure: 包含K线图和均线的plotly图表
        """
        fig = go.Figure()
        
        # 添加K线图
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='K线'
        ))
        
        # 添加移动平均线
        colors = ['blue', 'orange', 'green', 'red']
        for i, period in enumerate(ma_periods):
            if f'MA{period}' in df.columns:
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=df[f'MA{period}'],
                    mode='lines',
                    name=f'MA{period}',
                    line=dict(color=colors[i % len(colors)], width=1)
                ))
        
        fig.update_layout(
            title='K线图与移动平均线',
            xaxis_title='日期',
            yaxis_title='价格',
            xaxis_rangeslider_visible=False,
            hovermode='x unified'
        )
        
        return fig
    
    def plot_macd(self, df):
        """
        绘制MACD指标图
        
        参数:
            df: 包含MACD指标的DataFrame
        
        返回:
            go.Figure: 包含MACD指标的plotly图表
        """
        fig = go.Figure()
        
        # 添加MACD线
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['MACD'],
            mode='lines',
            name='MACD',
            line=dict(color='blue', width=1)
        ))
        
        # 添加信号线
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['MACD_Signal'],
            mode='lines',
            name='Signal',
            line=dict(color='red', width=1)
        ))
        
        # 添加柱状图
        fig.add_trace(go.Bar(
            x=df.index,
            y=df['MACD_Hist'],
            name='MACD Hist',
            marker_color= np.where(df['MACD_Hist'] >= 0, 'green', 'red')
        ))
        
        fig.update_layout(
            title='MACD指标',
            xaxis_title='日期',
            yaxis_title='MACD',
            hovermode='x unified'
        )
        
        return fig
    
    def plot_kdj(self, df):
        """
        绘制KDJ指标图
        
        参数:
            df: 包含KDJ指标的DataFrame
        
        返回:
            go.Figure: 包含KDJ指标的plotly图表
        """
        fig = go.Figure()
        
        # 添加K线
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['KDJ_K'],
            mode='lines',
            name='K',
            line=dict(color='blue', width=1)
        ))
        
        # 添加D线
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['KDJ_D'],
            mode='lines',
            name='D',
            line=dict(color='orange', width=1)
        ))
        
        # 添加J线
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['KDJ_J'],
            mode='lines',
            name='J',
            line=dict(color='green', width=1)
        ))
        
        # 添加超买超卖线
        fig.add_hline(y=20, line=dict(color='gray', dash='dash'), name='超卖线')
        fig.add_hline(y=80, line=dict(color='gray', dash='dash'), name='超买线')
        
        fig.update_layout(
            title='KDJ指标',
            xaxis_title='日期',
            yaxis_title='KDJ',
            yaxis_range=[0, 100],
            hovermode='x unified'
        )
        
        return fig
    
    def plot_rsi(self, df, timeperiod=14):
        """
        绘制RSI指标图
        
        参数:
            df: 包含RSI指标的DataFrame
            timeperiod: RSI计算周期
        
        返回:
            go.Figure: 包含RSI指标的plotly图表
        """
        fig = go.Figure()
        
        # 添加RSI线
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['RSI'],
            mode='lines',
            name=f'RSI({timeperiod})',
            line=dict(color='purple', width=1)
        ))
        
        # 添加超买超卖线
        fig.add_hline(y=30, line=dict(color='gray', dash='dash'), name='超卖线')
        fig.add_hline(y=70, line=dict(color='gray', dash='dash'), name='超买线')
        
        fig.update_layout(
            title=f'RSI({timeperiod})指标',
            xaxis_title='日期',
            yaxis_title='RSI',
            yaxis_range=[0, 100],
            hovermode='x unified'
        )
        
        return fig
    
    def plot_boll(self, df):
        """
        绘制布林带图
        
        参数:
            df: 包含布林带指标的DataFrame
        
        返回:
            go.Figure: 包含布林带指标的plotly图表
        """
        fig = go.Figure()
        
        # 添加收盘价
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['close'],
            mode='lines',
            name='收盘价',
            line=dict(color='blue', width=1)
        ))
        
        # 添加上轨
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['BOLL_Upper'],
            mode='lines',
            name='上轨',
            line=dict(color='red', width=1, dash='dash')
        ))
        
        # 添加中轨
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['BOLL_Middle'],
            mode='lines',
            name='中轨',
            line=dict(color='green', width=1)
        ))
        
        # 添加下轨
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['BOLL_Lower'],
            mode='lines',
            name='下轨',
            line=dict(color='red', width=1, dash='dash')
        ))
        
        fig.update_layout(
            title='布林带指标',
            xaxis_title='日期',
            yaxis_title='价格',
            hovermode='x unified'
        )
        
        return fig
    
    def plot_volume_obv(self, df):
        """
        绘制成交量与OBV指标图
        
        参数:
            df: 包含OBV指标的DataFrame
        
        返回:
            go.Figure: 包含成交量和OBV指标的plotly图表
        """
        # 创建子图
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)
        
        # 添加成交量柱状图
        fig.add_trace(go.Bar(
            x=df.index,
            y=df['volume'],
            name='成交量',
            marker_color=np.where(df['close'] >= df['open'], 'green', 'red')
        ), row=1, col=1)
        
        # 添加OBV线
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['OBV'],
            mode='lines',
            name='OBV',
            line=dict(color='blue', width=1)
        ), row=2, col=1)
        
        fig.update_layout(
            title='成交量与OBV指标',
            hovermode='x unified'
        )
        
        fig.update_yaxes(title_text='成交量', row=1, col=1)
        fig.update_yaxes(title_text='OBV', row=2, col=1)
        fig.update_xaxes(title_text='日期', row=2, col=1)
        
        return fig
    
    def plot_combined_charts(self, df):
        """
        绘制组合图表，包含K线图、MACD、KDJ、RSI和成交量
        
        参数:
            df: 包含所有技术指标的DataFrame
        
        返回:
            go.Figure: 包含组合图表的plotly图表
        """
        # 创建子图布局
        fig = make_subplots(
            rows=5, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=('K线图与移动平均线', 'MACD指标', 'KDJ指标', 'RSI指标', '成交量与OBV')
        )
        
        # 1. K线图与均线
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='K线'
        ), row=1, col=1)
        
        # 添加均线
        ma_periods = [5, 10, 20, 60]
        colors = ['blue', 'orange', 'green', 'red']
        for i, period in enumerate(ma_periods):
            if f'MA{period}' in df.columns:
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=df[f'MA{period}'],
                    mode='lines',
                    name=f'MA{period}',
                    line=dict(color=colors[i % len(colors)], width=1)
                ), row=1, col=1)
        
        # 2. MACD指标
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['MACD'],
            mode='lines',
            name='MACD',
            line=dict(color='blue', width=1)
        ), row=2, col=1)
        
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['MACD_Signal'],
            mode='lines',
            name='Signal',
            line=dict(color='red', width=1)
        ), row=2, col=1)
        
        fig.add_trace(go.Bar(
            x=df.index,
            y=df['MACD_Hist'],
            name='MACD Hist',
            marker_color=np.where(df['MACD_Hist'] >= 0, 'green', 'red')
        ), row=2, col=1)
        
        # 3. KDJ指标
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['KDJ_K'],
            mode='lines',
            name='K',
            line=dict(color='blue', width=1)
        ), row=3, col=1)
        
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['KDJ_D'],
            mode='lines',
            name='D',
            line=dict(color='orange', width=1)
        ), row=3, col=1)
        
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['KDJ_J'],
            mode='lines',
            name='J',
            line=dict(color='green', width=1)
        ), row=3, col=1)
        
        fig.add_hline(y=20, line=dict(color='gray', dash='dash'), name='超卖线', row=3, col=1)
        fig.add_hline(y=80, line=dict(color='gray', dash='dash'), name='超买线', row=3, col=1)
        
        # 4. RSI指标
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['RSI'],
            mode='lines',
            name='RSI',
            line=dict(color='purple', width=1)
        ), row=4, col=1)
        
        fig.add_hline(y=30, line=dict(color='gray', dash='dash'), name='超卖线', row=4, col=1)
        fig.add_hline(y=70, line=dict(color='gray', dash='dash'), name='超买线', row=4, col=1)
        
        # 5. 成交量与OBV
        fig.add_trace(go.Bar(
            x=df.index,
            y=df['volume'],
            name='成交量',
            marker_color=np.where(df['close'] >= df['open'], 'green', 'red')
        ), row=5, col=1)
        
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['OBV'],
            mode='lines',
            name='OBV',
            line=dict(color='blue', width=1)
        ), row=5, col=1)
        
        # 更新布局
        fig.update_layout(
            height=1200,
            width=1000,
            title_text='个股技术指标分析',
            hovermode='x unified',
            showlegend=False
        )
        
        # 更新坐标轴
        fig.update_xaxes(rangeslider_visible=False)
        fig.update_yaxes(title_text='价格', row=1, col=1)
        fig.update_yaxes(title_text='MACD', row=2, col=1)
        fig.update_yaxes(title_text='KDJ', row=3, col=1, range=[0, 100])
        fig.update_yaxes(title_text='RSI', row=4, col=1, range=[0, 100])
        fig.update_yaxes(title_text='成交量', row=5, col=1)
        
        return fig