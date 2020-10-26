import numpy as np
import pandas as pd

import talib


# engine = bellykit.bellykit_sql.login_guest('stock')

import os

datafile = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','data','workshop_data.csv'))

data0050 = pd.read_csv(datafile, header=None)
data0050.columns = ['date', 'symbol', 'open', 'high', 'low', 'close', 'volume', 'adj_open']
#data0050.columns = ['date', 'symbol', 'open', 'high', 'low', 'close', 'volume']
data0050.set_index('date', drop=True, inplace=True)


def get_price(*args):
    '''
    取得台灣50成分股的股價資訊。
    台灣50成分股：
    1101, 1102, 1216, 1301, 1303, 1326, 1402, 1802, 
    2002, 2105, 2201, 2207, 2311, 2324, 2801, 2880, 
    2881, 2882, 2883, 2885, 2886, 2890, 2891, 2892,
    5880, 2912, 1722, 6505, 2303, 2330, 2454, 2301, 
    2324, 2353, 2457, 2382, 3231, 2409, 3008, 3481, 
    3673, 2412, 2498, 3045, 4904, 2308, 2347, 2317,
    2354, 2474); 
    '''
    data = None
    for symbol in args:
        try:
            data[symbol]
            pass
        except KeyError:
            pass
        except TypeError:
            pass
        except Exception as e:
            raise e

        # price = bellykit.data_api.get_price(str(symbol), select=['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME'], start='20120101')
        # price.columns = price.columns.str.lower()
        
        price = data0050[data0050['symbol'] == symbol].copy()
        if len(price) == 0:
            print(f'no stock({symbol}) data')
            continue

        del price['symbol']
        # price.loc[:, ('adj_open')] = price.loc[:, ('open')].copy()
        # price['adj_open'] = price['open'].copy()

        # data type
        
        for col in ['open', 'high', 'low', 'close', 'adj_open']:
            try:
                price.loc[:,col].replace('N,N', method='ffill', inplace=True)
                price.loc[:,col] = price.loc[:, col].astype(float)
            except Exception as e:
                raise e


        # price.set_index('date', drop=True, inplace=True)
        col = [(symbol, i) for i in price.columns.to_list()]
        price.columns = pd.MultiIndex.from_tuples(col)
        try:
            data = pd.merge(left=data, right=price, on='date')
        except TypeError:
            data = price
        except Exception as e:
            raise e

    return data


class Price():
    def __init__(self, *args):
        self.data = get_price(*args)


    def MA(self, symbol, period, price='close'):
        name = f'MA{period}'
        ma_series = self.data[symbol, price].rolling(period).mean().fillna(0)
        ma_df = pd.DataFrame(ma_series)
        ma_df.columns = pd.MultiIndex.from_tuples([(symbol, name)])
        self.data[(symbol, name)] = ma_df
        # data = data.sort_index(axis=1)
        self.sort_columns()
        return
    
    def RSI(self, symbol, period, price='close'):
        name = f'RSI{period}'
        rsi_series = talib.RSI(self.data[symbol, 'close'], timeperiod=period).fillna(0)
        self.data[symbol, name] = rsi_series
        # rsi_df = pd.DataFrame(rsi_series)
        # rsi_df.columns = pd.MultiIndex.from_tuples([(symbol, name)])
        # self.data[(symbol, name)] = rsi_df
        self.sort_columns()
        return
    
    def KD(self, symbol, rsv_period=9, k_period=3, d_period=3, price='close'):
        ll = self.data[symbol, 'low'].rolling(rsv_period, min_periods=1).min()
        hh = self.data[symbol, 'high'].rolling(rsv_period, min_periods=1).max()
        RSV = (self.data[symbol, 'close'] - ll) / (hh - ll)
        fD = RSV.ewm(com=k_period-1, min_periods=1).mean()
        sK = fD.copy()
        sD = sK.ewm(com=d_period-1, min_periods=1).mean()
    
        self.data[symbol, f'K{rsv_period}'] = sK
        self.data[symbol, f'D{rsv_period}'] = sD
    
        kds = pd.DataFrame({'RSV': RSV, 'fD': fD})
        self.sort_columns()
        return kds
    
    def crossover(self, symbol, ind1, ind2):
        name = f'{ind1}x{ind2}'
        c1 = self.data[symbol, ind1] > self.data[symbol, ind2]
        c2 = (~c1).shift(1, fill_value=False)
        crossover_series = (c1&c2)
        self.data[symbol, name] = crossover_series
        self.sort_columns()
        return
    
    def get_random_data(self, *args):
        self.data = np.random.random(10, 4)
        return self.data
    
    
    def sort_columns(self):
        columns = np.array(self.data.columns)
        symbols = [i[0] for i in columns]
        sorted_columns = columns[np.argsort(symbols)]
    
        new_columns = pd.MultiIndex.from_tuples(sorted_columns)
        self.data = self.data[new_columns]
        
    
    
