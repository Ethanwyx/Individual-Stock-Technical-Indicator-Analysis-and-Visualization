import talib
import numpy as np
import pandas as pd

class TechnicalIndicators:
    def __init__(self):
        pass
    
    def calculate_ma(self, df, periods=[5, 10, 20, 60]):
        """
        计算移动平均线
        
        参数:
            df: 包含股票数据的DataFrame
            periods: 要计算的均线周期列表
        
        返回:
            pd.DataFrame: 包含原数据和均线的DataFrame
        """
        for period in periods:
            df[f'MA{period}'] = talib.MA(df['close'], timeperiod=period)
        return df
    
    def calculate_macd(self, df, fastperiod=12, slowperiod=26, signalperiod=9):
        """
        计算MACD指标
        
        参数:
            df: 包含股票数据的DataFrame
            fastperiod: 快速EMA周期
            slowperiod: 慢速EMA周期
            signalperiod: 信号线EMA周期
        
        返回:
            pd.DataFrame: 包含MACD指标的DataFrame
        """
        macd, macdsignal, macdhist = talib.MACD(df['close'], fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
        df['MACD'] = macd
        df['MACD_Signal'] = macdsignal
        df['MACD_Hist'] = macdhist
        return df
    
    def calculate_kdj(self, df, n=9, m1=3, m2=3):
        """
        计算KDJ指标
        
        参数:
            df: 包含股票数据的DataFrame
            n: RSV计算周期
            m1: K值平滑周期
            m2: D值平滑周期
        
        返回:
            pd.DataFrame: 包含KDJ指标的DataFrame
        """
        # 复制数据，避免修改原数据
        df_copy = df.copy()
        
        # 手动计算RSV：(收盘价 - 最近N日最低价) / (最近N日最高价 - 最近N日最低价) * 100
        highest = df_copy['high'].rolling(window=n).max()
        lowest = df_copy['low'].rolling(window=n).min()
        
        # 避免除以零
        delta = highest - lowest
        delta = delta.fillna(1)  # 填充NaN值
        delta[delta == 0] = 1
        
        rsv = (df_copy['close'] - lowest) / delta * 100
        
        # 初始化K、D值
        k_values = [50.0] * len(df_copy)  # 初始值设为50
        d_values = [50.0] * len(df_copy)
        
        # 计算K、D值
        for i in range(1, len(df_copy)):
            if not pd.isna(rsv.iloc[i]):
                # K值 = 前一日K值 * (m1-1)/m1 + 当日RSV * 1/m1
                k_values[i] = k_values[i-1] * (m1 - 1) / m1 + rsv.iloc[i] * 1 / m1
                # D值 = 前一日D值 * (m2-1)/m2 + 当日K值 * 1/m2
                d_values[i] = d_values[i-1] * (m2 - 1) / m2 + k_values[i] * 1 / m2
            else:
                # 如果RSV是NaN，使用前一日的值
                k_values[i] = k_values[i-1]
                d_values[i] = d_values[i-1]
        
        # 计算J值：J = 3*K - 2*D
        k_series = pd.Series(k_values, index=df_copy.index)
        d_series = pd.Series(d_values, index=df_copy.index)
        j_series = 3 * k_series - 2 * d_series
        
        # 将计算结果添加到原DataFrame
        df['KDJ_K'] = k_series
        df['KDJ_D'] = d_series
        df['KDJ_J'] = j_series
        
        return df
    
    def calculate_rsi(self, df, timeperiod=14):
        """
        计算RSI指标
        
        参数:
            df: 包含股票数据的DataFrame
            timeperiod: RSI计算周期
        
        返回:
            pd.DataFrame: 包含RSI指标的DataFrame
        """
        df['RSI'] = talib.RSI(df['close'], timeperiod=timeperiod)
        return df
    
    def calculate_boll(self, df, timeperiod=20, nbdevup=2, nbdevdn=2):
        """
        计算布林带指标
        
        参数:
            df: 包含股票数据的DataFrame
            timeperiod: 计算周期
            nbdevup: 上轨标准差倍数
            nbdevdn: 下轨标准差倍数
        
        返回:
            pd.DataFrame: 包含布林带指标的DataFrame
        """
        upper, middle, lower = talib.BBANDS(df['close'], timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn, matype=0)
        df['BOLL_Upper'] = upper
        df['BOLL_Middle'] = middle
        df['BOLL_Lower'] = lower
        return df
    
    def calculate_obv(self, df):
        """
        计算OBV指标
        
        参数:
            df: 包含股票数据的DataFrame
        
        返回:
            pd.DataFrame: 包含OBV指标的DataFrame
        """
        df['OBV'] = talib.OBV(df['close'], df['volume'])
        return df
    
    def calculate_all_indicators(self, df):
        """
        计算所有技术指标
        
        参数:
            df: 包含股票数据的DataFrame
        
        返回:
            pd.DataFrame: 包含所有技术指标的DataFrame
        """
        df = self.calculate_ma(df)
        df = self.calculate_macd(df)
        df = self.calculate_kdj(df)
        df = self.calculate_rsi(df)
        df = self.calculate_boll(df)
        df = self.calculate_obv(df)
        return df