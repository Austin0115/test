import pyupbit
import numpy as np
from scipy.ndimage import gaussian_filter1d

# OHLCV(open, high, low, close, volume)로 당일 시가, 고가, 저가, 종가, 거래량에 대한 데이터
# df = pyupbit.get_ohlcv("KRW-BTC", count=7)
# df_pre = pyupbit.get_ohlcv("KRW-BTC", count=7)
# df_pre.to_excel("save1.xlsx")

#어제까지의 data 획득
df_pre = pyupbit.get_ohlcv("KRW-BTC", interval="minute240")[:196]
df_pre.to_excel("pre_data.xlsx")

df = pyupbit.get_ohlcv("KRW-BTC", interval="minute60")[186:]
df.to_excel("data.xlsx")

df_pre['average'] = (df_pre['high'] + df_pre['low']) * 0.5
df['gaussian'] = gaussian_filter1d(df['average'], 1.1)

# target(매수가), range 컬럼을 한칸씩 밑으로 내림(.shift(1))
# df['target'] = df['open'] + df['range'].shift(1)
df['target_sell'] = df['gaussian'].shift(1) * 1.008
df['target_buy'] = df['gaussian'].shift(1) * 0.992