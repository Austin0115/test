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

df.to_excel("save.xlsx")
fee = 0.005
money = 0.0
total = 0.0
ror = 0.0

# ror(수익률), np.where(조건문, 참일때 값, 거짓일때 값)
for i in range(len(df['average'])):
    if money == 0 and df['low'][i] < df['target_buy'][i] :
        money = df['target_buy'][i]
        print('buy',i,df['target_buy'][i])
    elif money != 0 and df['high'][i] > df['target_sell'][i]:
        total += df['target_sell'][i] - money    
        ror += df['target_sell'][i]/money-fee 
        print('sell',i,df['target_sell'][i])
        money = 0
print(ror)
# df['ror'] = np.where(df['high'] > df['target'],
#                      df['close'] / df['target'] - fee,
#                      1)

# 누적 곱 계산(cumprod) => 누적 수익률
# df['hpr'] = df['ror'].cumprod()

# # Draw Down 계산 (누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100)
# df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# #MDD 계산
# print("MDD(%): ", df['dd'].max())

#엑셀로 출력
# df.to_excel("dd.xlsx")