import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk
import yfinance as yf

import mpl_finance as mpf
import matplotlib.dates as mdates

import plotly.graph_objects as go
import plotly.subplots as sp
import matplotlib.pyplot as plt

from Trading_main import *

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

import pandas as pd
import numpy as np

start_date = "2022-01-01"
end_date = "2023-01-01"
stock = 'AAPL'
allStocks = {}
df =  yf.download(stock, start=start_date, end=end_date)
allStocks[stock] = df
quotes = zip(mdates.date2num(df.index.to_pydatetime()), df['Open'], df['High'], df['Low'], df['Close'])

fig = Figure(figsize=(5, 5), dpi=100)
a = fig.add_subplot(111)
a.set_title(stock)

def animate(i):
    if stock in allStocks:
        df = allStocks[stock]
        print('stock already downloaded')
    else:
        df =  yf.download(stock, start=start_date, end=end_date)
        print('downloading stock')
        
    quotes = zip(mdates.date2num(df.index.to_pydatetime()), df['Open'], df['High'], df['Low'], df['Close'])
    mpf.candlestick_ohlc(a, quotes, width=0.6, colorup='g', colordown='r')
    a.xaxis.set_major_locator(mdates.AutoDateLocator())
    a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()


class TradingGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Trading GUI")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (PageOne, GraphPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(PageOne)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        def get_text():
            # Get the text from the input box
            global stock
            global start_date
            global end_date
            start_date = start_date_entry.get()
            end_date = end_date_entry.get()
            stock = stock_entry.get()

        def submit_and_show_frame():
            global quotes
            get_text()
            a.clear()
            a.set_title(stock)
            df = yf.download(stock, start=start_date, end=end_date)
            quotes = zip(mdates.date2num(df.index.to_pydatetime()), df['Open'], df['High'], df['Low'], df['Close'])
            controller.show_frame(GraphPage)

        def runAnalyseLastMonth():
            global allStocks
            allStocks = analyseLastMonth()
            
        # Create a label and entry for stock ticker
        stock_label = ttk.Label(self, text="Stock Ticker:")
        stock_entry = ttk.Entry(self)
        # Set a placeholder for stock entry
        stock_entry.insert(0, "AAPL")
        stock_label.pack(pady=10, padx=10)
        stock_entry.pack()

        # Create a label and entry for start date
        start_date_label = ttk.Label(self, text="Start Date (YYYY-MM-DD):")
        start_date_entry = ttk.Entry(self)
        # Set a placeholder for start date entry
        start_date_entry.insert(0, start_date)
        start_date_label.pack(pady=10, padx=10)
        start_date_entry.pack()

        # Create a label and entry for end date
        end_date_label = ttk.Label(self, text="End Date (YYYY-MM-DD):")
        end_date_entry = ttk.Entry(self)
        # Set a placeholder for end date entry
        end_date_entry.insert(0, end_date)
        end_date_label.pack(pady=10, padx=10)
        end_date_entry.pack()
        
        # Create a submit button
        submit_button = ttk.Button(self, text="Submit", command = submit_and_show_frame)
        submit_button.pack()

        buttonRun = ttk.Button(
            self, text="Run analysis for stock", command= lambda:runScript(stock,start_date,end_date)
        )
        buttonRun.pack()
        
        buttonRunAll = ttk.Button(
            self, text="Run script for all stocks", command= lambda:runAnalyseLastMonth()
        )
        buttonRunAll.pack()      
        

class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(
            self, text="Back to Home", command=lambda: controller.show_frame(PageOne)
        )
        button1.pack()     
        
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = TradingGUI()
ani = animation.FuncAnimation(fig, animate, interval=1000)
app.mainloop()
