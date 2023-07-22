## Import libraries
import plotly.graph_objects as go
import plotly.io as pio

from scipy.signal import find_peaks
from datetime import datetime

import yfinance as yf
import numpy as np


print("libraries imported"); #--------------------------------------------------------------------------------
pio.renderers.default='browser'


stock = 'AAPL'

start_date = datetime(2019, 1, 1)
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

)

print("Graph created")#--------------------------------------------------------------------------------

## Find maximum values

close_prices = df['Close']
peaks, _ = find_peaks(close_prices, distance=30)
peak_values = close_prices[peaks]

for i in range(len(peaks)):
    peakDate = df.index[peaks[i]].strftime('%Y-%m-%d') # convert index position to date
    layout.add_vline( # add vertical line
        x=peakDate,
        line=dict(color='red', width=1, dash='dot')
    )             
    
layout.show()
print("Added vertical lines at peaks") #---------------------------------------------------------------


# Find adjacent peaks within a distance of 3 peaks
adjacent_peaks = []
for i in range(len(peaks)):
    for j in range(i+1, len(peaks)):
        if peaks[j] - peaks[i] <= 3:
            adjacent_peaks.append((peaks[i], peaks[j]))


## Fit line through at least 3 peaks with an error margin of 10%
min_peaks = 3
error_margin = 0.1

for i in range(len(peaks)-min_peaks):
    x = peaks[i:i+min_peaks+1]
    y = close_prices[x]
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    if np.all(np.abs((p(x)-y)/y) < error_margin):
        layout.add_trace(go.Scatter(
            x=x,
            y=p(x),
            mode='lines',
            name='Line fit through peaks ' + ', '.join(str(j) for j in x)
        ))

## Fit lines through sets of peaks that are adjacent or a maximum of 3 peaks apart
max_peak_distance = 3

peak_groups = np.split(peaks, np.where(np.diff(peaks) > max_peak_distance)[0]+1)

for group in peak_groups:
    if len(group) >= 2:
        x = group
        y = close_prices[x]
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        layout.add_trace(go.Scatter(
            x=x,
            y=p(x),
            mode='lines',
            name='Line fit through peaks ' + ', '.join(str(j) for j in x)
        ))

## Create graph
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
    data=[graph],
    layout_title=stock + " Stock"
)

## Add vertical lines at peaks
for i in range(len(peaks)):
    peak_date = df.index[peaks[i]].strftime('%Y-%m-%d')
    layout.add_vline(
        x=peak_date,
        line=dict(color='red', width=1, dash='dot')
    )

layout.show()
print("Graph created")








# Fit a straight line through adjacent peaks
for i, j in adjacent_peaks:
    x = np.arange(i, j+1)
    y = close_prices[i:j+1]
    if len(x) >= 2:
        slope, intercept = np.polyfit(x, y, deg=1)
        x_range = np.arange(i, j+2)
        y_range = slope * x_range + intercept
        layout.add_trace(go.Scatter(
            x=x_range,
            y=y_range,
            mode='lines',
            name='Line of Peaks',
            line=dict(color='green', width=2, dash='dash')
        ))

layout.show()
print("Added lines through adjacent peaks")

