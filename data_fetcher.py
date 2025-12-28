import akshare as ak
import pandas as pd
import os
from datetime import datetime

class DataFetcher:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
    
    def fetch_stock_data(self, symbol, start_date, end_date):
        """
        获取股票历史行情数据
        
        参数:
            symbol: 股票代码，如 '600000'
            start_date: 开始日期，格式 'YYYY-MM-DD'
            end_date: 结束日期，格式 'YYYY-MM-DD'
        
        返回:
            pd.DataFrame: 包含股票历史行情数据的DataFrame
        """
        # 构建文件名
        file_name = f"{symbol}_{start_date}_{end_date}.csv"
        file_path = os.path.join(self.data_dir, file_name)
        
        # 检查文件是否已存在
        if os.path.exists(file_path):
            print(f"从本地加载数据: {file_path}")
            df = pd.read_csv(file_path, index_col='date', parse_dates=True)
            return df
        
        # 从akshare获取数据
        print(f"从akshare获取数据: {symbol} {start_date} 到 {end_date}")
        try:
            # 尝试不同的akshare接口
            # 接口1: stock_zh_a_hist
            print(f"正在调用ak.stock_zh_a_hist，股票代码: {symbol}")
            df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
            
            # 如果接口1返回空数据，尝试接口2: stock_zh_a_daily
            if df.empty:
                print("接口1返回空数据，尝试调用ak.stock_zh_a_daily...")
                df = ak.stock_zh_a_daily(symbol=f"sh{symbol}", start_date=start_date, end_date=end_date)
            
            # 如果接口2返回空数据，尝试接口3: stock_zh_a_spot
            if df.empty:
                print("接口2返回空数据，尝试调用ak.stock_zh_a_spot...")
                # 这个接口只能获取最新数据
                df = ak.stock_zh_a_spot()
                if not df.empty:
                    # 过滤指定股票
                    df = df[df['代码'] == symbol]
            
            # 调试：打印数据基本信息
            print(f"数据形状: {df.shape}")
            print(f"数据列名: {df.columns.tolist()}")
            print(f"数据前5行: {df.head()}")
            
            # 检查数据是否为空
            if df.empty:
                print("所有接口获取的数据都为空")
                return None
            
            # 数据处理
            if '日期' in df.columns:
                df.rename(columns={'日期': 'date', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low', '成交量': 'volume'}, inplace=True)
            elif 'date' in df.columns:
                # 已经有date列，无需重命名
                pass
            elif 'trade_date' in df.columns:
                df.rename(columns={'trade_date': 'date'}, inplace=True)
            elif len(df.columns) >= 6:
                # 如果没有明确的日期列，尝试按位置命名
                df.columns = ['date', 'open', 'close', 'high', 'low', 'volume', 'amount', 'change', 'change_pct', 'turnover_rate']
            
            # 确保date列存在
            if 'date' not in df.columns:
                print("数据中没有日期列")
                return None
            
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            
            # 保存到本地
            df.to_csv(file_path)
            print(f"数据已保存到: {file_path}")
            
            return df
        except Exception as e:
            print(f"获取数据失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_stock_info(self, symbol):
        """
        获取股票基本信息
        
        参数:
            symbol: 股票代码
        
        返回:
            dict: 股票基本信息
        """
        try:
            stock_info = ak.stock_individual_info_em(symbol=symbol)
            return stock_info
        except Exception as e:
            print(f"获取股票信息失败: {e}")
            return None

if __name__ == "__main__":
    # 测试数据获取功能
    fetcher = DataFetcher()
    df = fetcher.fetch_stock_data('600000', '2023-01-01', '2023-12-31')
    if df is not None:
        print(df.head())