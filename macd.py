from datetime import timedelta
import pandas as pd
from plotly.subplots import make_subplots
from stockstats import StockDataFrame as Sdf
import plotly.graph_objects as go

data = pd.read_csv('binance_BTCUSDT_1m.txt')

stock = Sdf.retype(data)
data['signal'] = stock['macds']
data['macd'] = stock['macd']
data['hist'] = stock['macdh']

rsi_6 = stock["rsi_6"]
rsi_12 = stock["rsi_12"]

data = data.tail(10080)
data['time'] = pd.to_datetime(data['time'], unit='s')
data['time'] = data['time'] + timedelta(hours=3)


#  The MACD that need to cross the signal line
#                                              to give you a Buy/Sell signal
#listLongShort = ["No data"]    # Since you need at least two days in the for loop

config = dict({'scrollZoom': True,
               'displaylogo': False})

fig = make_subplots(shared_xaxes=True, rows=4, cols=1, row_heights=[0.6, 0.15, 0.3, 0.3],
                    vertical_spacing=0.009, horizontal_spacing=0.009)
fig['layout']['margin'] = {'l': 30, 'r': 10, 'b': 50, 't': 25}
fig.add_trace(go.Candlestick(
        x=data['time'],
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close'], name='candlestick'), row=1, col=1)
fig.update_xaxes(rangeslider_visible=False)
ap = fig.add_trace(go.Scatter(name='macd', x=data['time'], y=data['macd'], line=dict(color='blue')), row=3, col=1)
ap1 = fig.add_trace(go.Scatter(name='signal', x=data['time'], y=data['signal'], line=dict(color='orange')), row=3, col=1)
ap2 = fig.add_trace(go.Bar(name='histogram', x=data['time'], y=data['hist'], marker_color='green'), row=2, col=1)
ap2.update_layout(barmode='stack')
fig.update_layout(template='plotly_dark')
ap3 = fig.add_trace(go.Scatter(x=data['time'], y=list(rsi_6), name="RSI 6 Day"), row=4, col=1)

fig.show(config=config)

#for i in range(1, len(signal)):
    #                          # If the MACD crosses the signal line upward
 #   if macd[i] > signal[i] and macd[i - 1] <= signal[i - 1]:
      #  listLongShort.append("BUY")
    #                          # The other way around
  #  elif macd[i] < signal[i] and macd[i - 1] >= signal[i - 1]:
     #   listLongShort.append("SELL")
    #                          # Do nothing if not crossed
   # else:
    #    listLongShort.append("HOLD")

#stock['Advice'] = listLongShort

# The advice column means "Buy/Sell/Hold" at the end of this day or
#  at the beginning of the next day, since the market will be closed

#print(stock['Advice'])