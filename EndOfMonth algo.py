import plotly.graph_objects as go
import plotly.io as pio

from scipy.signal import find_peaks
from pandas_datareader.nasdaq_trader import get_nasdaq_symbols
from datetime import datetime

import yfinance as yf

print("libraries imported"); #--------------------------------------------------------------------------------
pio.renderers.default='browser'


symbols = get_nasdaq_symbols()
stock = 'AAPL'

start_date = datetime(2000, 1, 1)
end_date = datetime.today()

print("Parameters defined");#--------------------------------------------------------------------------------
## download and format stock data
df = yf.download(stock, start=start_date, end=end_date)

print("Data downloaded");#--------------------------------------------------------------------------------

graph = {
    'x': df.index,
    'open': df.Open,
    'close': df.Close,
    'high': df.High,
    'low': df.Low,
    'type': 'candlestick',
    'name': stock,
    'showlegend': True
}

layout = go.Figure(
    data = [graph],
    layout_title= stock +" Stock"

go.show()

df['numbering'] = range(1,len(df) + 1)
EOMValues = []
BOMValues = []
diff = 0
for i in range(1,len(df)-1):
    diff = df.Close[i] - df.Close[i-1]
    if df.index[i].day > 0 and df.index[i].day < 26:
        EOMValues.append(diff)
    elif df.index[i].day >= 26 and df.index[i].day <= 31:
        BOMValues.append(diff)

Day25 = []
Day3 = []
for i in range(1,len(df)-1):
    if df.index[i].day == 25:
        Day25 = df.Close[i]
    if df.index[i].day == 3:
         Day3 = df.Close[i]

    avgEOM = (Day3 - Day25) / 8
    avgRest = (Day25 - Day3) / 25


sum(EOMValues)/len(EOMValues)
sum(BOMValues)/len(BOMValues)