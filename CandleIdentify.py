# import plotly.graph_objects as go
# import plotly.io as pio

# from scipy.signal import find_peaks
# from datetime import datetime

# import pandas as pd
# import yfinance as yf

# from datetime import timedelta

# # --------------------------------------------------------------------------------
# print("libraries imported")
# pio.renderers.default = 'browser'

# stock = 'AAPL'

# start_date = datetime(2000, 1, 1)
# end_date = datetime.today()

# # --------------------------------------------------------------------------------
# print("Parameters defined")

# # download and format stock data
# df = yf.download(stock, start=start_date, end=end_date)

# # --------------------------------------------------------------------------------
# print("Data downloaded")

# graph = {
#     'x': df.index,
#     'open': df.Open,
#     'close': df.Close,
#     'high': df.High,
#     'low': df.Low,
#     'type': 'candlestick',
#     'name': stock,
#     'showlegend': True
# }

# layout = go.Figure(
#     data=[graph],
#     layout_title=stock + " Stock"
# )

# layout.show()


# (df['Candle_Type'] =='Hammer').sum()
# (df['Candle_Type'] =='doji').sum()

# allStocks = analyseLastMonth()
# stars = findStars(stockList, allStocks)
# [negatives, positives] = backtestStar(allStocks[0])

                


def candleSizes(candle):
    # determines the sizes the body and tails of each candle
    body = candle.Close - candle.Open
    topTail = 0
    bottomTail = 0

    if (body > 0):
        bottomTail = candle.Open - candle.Low
        topTail = candle.High - candle.Close
    if (body < 0):
        bottomTail = candle.Close - candle.Low
        topTail = candle.High - candle.Open

    if topTail == 0:
        topTail = 0.0001
    if bottomTail == 0:
        bottomTail = 0.0001

    lengths = {
        'body': body,
        'topTail': topTail,
        'bottomTail': bottomTail
    }
    return lengths



def candleIdentifier(lengths):
    # Identify the type of candle based on body and tail size
    # Possibilities: Doji, spinning_top, hammer, inverse_hammer, hanging_man, shooting_star, bullish_marubozu, bearish_marubozu, noraml_bullish, normal_bearish, unkown

    topTail = lengths['topTail']
    bottomTail = lengths['bottomTail']
    body = lengths['body']
    x = 0.05  # doji factor
    y = 0.2  # hammer/star factor

    # doji's
    if (abs(body)/bottomTail < x or abs(body)/topTail < x):
        candleType = 'doji'
    elif (abs(body)/bottomTail < y and abs(body)/topTail < y):
        candleType = 'Spinning_top'
    elif (body > 0 and topTail < x and abs(body)/bottomTail < y):
        candleType = 'Hammer'
    elif (body > 0 and bottomTail < x and abs(body)/topTail < y):
        candleType = 'Inverse_Hammer'
    elif (body < 0 and topTail < x and abs(body)/bottomTail < y):
        candleType = 'Hanging_man'
    elif (body < 0 and bottomTail < x and abs(body)/topTail < y):
        candleType = 'Shooting star'
    elif (body > 0 and topTail/abs(body) < y and bottomTail/abs(body) < y):
        candleType = 'Bullish_Marubozu'
    elif (body < 0 and topTail/abs(body) < y and bottomTail/abs(body) < y):
        candleType = 'Bearish_Marubozu'
    elif (body > 0) and topTail/abs(body) > y and bottomTail/abs(body) > y:
        candleType = 'Normal_Bullish'
    elif (body < 0 and topTail/abs(body) > y and bottomTail/abs(body) > y):
        candleType = 'Normal_Bearish'
    elif (topTail == 0 or bottomTail == 0):
        candleType = 'Divide by 0'
    else:
        candleType = 'Unknown'

    return candleType


def checkStar(candle1, candle2, candle3):
    # Morning star pattern
    # Conditions:
    # 1: Downtrend (we're looking for a bullish reversal)
    # 2: First candle should be a big bearish candle
    # 3: Second candle should have a small body (indicates indecisiveness)
    # 4: Third candle should be a big bullish candle (confirming the trend reversal)
    star = ''
    if (candle1.body < 0 and abs(candle2.body) < abs(candle1.body) and candle3.body > 0 and
        candle1.Close > candle2.Open and candle1.Close > candle2.Close and
            candle2.Close < candle3.Open and candle2.Open < candle3.Open):
        #print('Morning star pattern found')
        star = 'Morning star'

    if (candle1.body > 0 and abs(candle2.body) < abs(candle1.body) and candle3.body < 0 and
        candle1.Close < candle2.Open and candle1.Close < candle2.Close and
            candle2.Close > candle3.Open and candle2.Open > candle3.Open):
        #print('Evening star pattern found')
        star = 'Evening star'

    return star


def findStars(stockList, allStocks):
    stars = []
    for i in range(0,len(stockList)-1):
        stock = stockList[i]
        stockData = allStocks[stock]
    
        try:
            for j in range(0,len(stockData) - 1):
                if (stockData['star'][j] != ''):
                        stars.append([stock, stockData['star'].index[j]])
        except:
            print('oops, no data for', stock)
    
    return stars


def loop3(df):
    # loops through all candle sets of 3 candles and determines if a star pattern is present
    star = list()
    for i in range(0, len(df) - 2):
        candle1 = df.iloc[i]
        candle2 = df.iloc[i + 1]
        candle3 = df.iloc[i + 2]
        star.append(checkStar(candle1, candle2, candle3))

    star.append('')
    star.append('')
    return star


def backtestStar(df):
    # when a star pattern is identified, this function checks if the stock moved up or down afterwards
    truePositives = []
    trueNegatives = []
    falsePositives = []
    falseNegatives = []
    diff = []
    
    for i in range(0, len(df) - 11):
        if (df['star'][i] == 'Morning star'):
            print('morning star found')
            diff.append(df['Close'][i+10] - df['Close'][i])
            if (df['Close'][i+10] > df['Close'][i]):
                truePositives.append(df.index[i])
            else:
                print('wrong direction')
                falsePositives.append(df.index[i])
        elif (df['star'][i] == 'Evening star'):   
            print('evening star found')
            diff.append(df['Close'][i+10] - df['Close'][i])
            if (df['Close'][i+10] > df['Close'][i]):
                trueNegatives.append(df.index[i])
            else:
                print('wrong direction')
                falseNegatives.append(df.index[i])
                
    return truePositives, trueNegatives, falsePositives, falseNegatives, diff

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# End of month values

# df['numbering'] = range(1,len(df) + 1)
# EOMValues = []
# BOMValues = []
# diff = 0
# for i in range(1,len(df)-1):
#     diff = df.Close[i] - df.Close[i-1]
#     if df.index[i].day > 0 and df.index[i].day < 26:
#         EOMValues.append(diff)
#     elif df.index[i].day >= 26 and df.index[i].day <= 31:
#         BOMValues.append(diff)

# Day25 = []
# Day3 = []
# for i in range(1,len(df)-1):
#     if df.index[i].day == 25:
#         Day25 = df.Close[i]
#     if df.index[i].day == 3:
#          Day3 = df.Close[i]

#     avgEOM = (Day3 - Day25) / 8
#     avgRest = (Day25 - Day3) / 25


# sum(EOMValues)/len(EOMValues)
# sum(BOMValues)/len(BOMValues)

stockList = (
'A',
'AAL',
'AAP',
'AAPL',
'ABBV',
'ABC',
'ABT',
'ACGL',
'ACN',
'ADBE',
'ADI',
'ADM',
'ADP',
'ADSK',
'AEE',
'AEP',
'AES',
'AFL',
'AIG',
'AIZ',
'AJG',
'AKAM',
'ALB',
'ALGN',
'ALK',
'ALL',
'ALLE',
'AMAT',
'AMCR',
'AMD',
'AME',
'AMGN',
'AMP',
'AMT',
'AMZN',
'ANET',
'ANSS',
'AON',
'AOS',
'APA',
'APD',
'APH',
'APTV',
'ARE',
'ATO',
'ATVI',
'AVB',
'AVGO',
'AVY',
'AWK',
'AXON',
'AXP',
'AZO',
'BA',
'BAC',
'BALL',
'BAX',
'BBWI',
'BBY',
'BDX',
'BEN',
'BF.B',
'BG',
'BIIB',
'BIO',
'BK',
'BKNG',
'BKR',
'BLK',
'BMY',
'BR',
'BRK.B',
'BRO',
'BSX',
'BWA',
'BXP',
'C',
'CAG',
'CAH',
'CARR',
'CAT',
'CB',
'CBOE',
'CBRE',
'CCI',
'CCL',
'CDAY',
'CDNS',
'CDW',
'CE',
'CEG',
'CF',
'CFG',
'CHD',
'CHRW',
'CHTR',
'CI',
'CINF',
'CL',
'CLX',
'CMA',
'CMCSA',
'CME',
'CMG',
'CMI',
'CMS',
'CNC',
'CNP',
'COF',
'COO',
'COP',
'COST',
'CPB',
'CPRT',
'CPT',
'CRL',
'CRM',
'CSCO',
'CSGP',
'CSX',
'CTAS',
'CTLT',
'CTRA',
'CTSH',
'CTVA',
'CVS',
'CVX',
'CZR',
'D',
'DAL',
'DD',
'DE',
'DFS',
'DG',
'DGX',
'DHI',
'DHR',
'DIS',
'DISH',
'DLR',
'DLTR',
'DOV',
'DOW',
'DPZ',
'DRI',
'DTE',
'DUK',
'DVA',
'DVN',
'DXC',
'DXCM',
'EA',
'EBAY',
'ECL',
'ED',
'EFX',
'EIX',
'EL',
'ELV',
'EMN',
'EMR',
'ENPH',
'EOG',
'EPAM',
'EQIX',
'EQR',
'EQT',
'ES',
'ESS',
'ETN',
'ETR',
'ETSY',
'EVRG',
'EW',
'EXC',
'EXPD',
'EXPE',
'EXR',
'F',
'FANG',
'FAST',
'FCX',
'FDS',
'FDX',
'FE',
'FFIV',
'FICO',
'FIS',
'FISV',
'FITB',
'FLT',
'FMC',
'FOX',
'FOXA',
'FRT',
'FSLR',
'FTNT',
'FTV',
'GD',
'GE',
'GEHC',
'GEN',
'GILD',
'GIS',
'GL',
'GLW',
'GM',
'GNRC',
'GOOG',
'GOOGL',
'GPC',
'GPN',
'GRMN',
'GS',
'GWW',
'HAL',
'HAS',
'HBAN',
'HCA',
'HD',
'HES',
'HIG',
'HII',
'HLT',
'HOLX',
'HON',
'HPE',
'HPQ',
'HRL',
'HSIC',
'HST',
'HSY',
'HUM',
'HWM',
'IBM',
'ICE',
'IDXX',
'IEX',
'IFF',
'ILMN',
'INCY',
'INTC',
'INTU',
'INVH',
'IP',
'IPG',
'IQV',
'IR',
'IRM',
'ISRG',
'IT',
'ITW',
'IVZ',
'J',
'JBHT',
'JCI',
'JKHY',
'JNJ',
'JNPR',
'JPM',
'K',
'KDP',
'KEY',
'KEYS',
'KHC',
'KIM',
'KLAC',
'KMB',
'KMI',
'KMX',
'KO',
'KR',
'L',
'LDOS',
'LEN',
'LH',
'LHX',
'LIN',
'LKQ',
'LLY',
'LMT',
'LNC',
'LNT',
'LOW',
'LRCX',
'LUV',
'LVS',
'LW',
'LYB',
'LYV',
'MA',
'MAA',
'MAR',
'MAS',
'MCD',
'MCHP',
'MCK',
'MCO',
'MDLZ',
'MDT',
'MET',
'META',
'MGM',
'MHK',
'MKC',
'MKTX',
'MLM',
'MMC',
'MMM',
'MNST',
'MO',
'MOH',
'MOS',
'MPC',
'MPWR',
'MRK',
'MRNA',
'MRO',
'MS',
'MSCI',
'MSFT',
'MSI',
'MTB',
'MTCH',
'MTD',
'MU',
'NCLH',
'NDAQ',
'NDSN',
'NEE',
'NEM',
'NFLX',
'NI',
'NKE',
'NOC',
'NOW',
'NRG',
'NSC',
'NTAP',
'NTRS',
'NUE',
'NVDA',
'NVR',
'NWL',
'NWS',
'NWSA',
'NXPI',
'O',
'ODFL',
'OGN',
'OKE',
'OMC',
'ON',
'ORCL',
'ORLY',
'OTIS',
'OXY',
'PARA',
'PAYC',
'PAYX',
'PCAR',
'PCG',
'PEAK',
'PEG',
'PEP',
'PFE',
'PFG',
'PG',
'PGR',
'PH',
'PHM',
'PKG',
'PKI',
'PLD',
'PM',
'PNC',
'PNR',
'PNW',
'PODD',
'POOL',
'PPG',
'PPL',
'PRU',
'PSA',
'PSX',
'PTC',
'PWR',
'PXD',
'PYPL',
'QCOM',
'QRVO',
'RCL',
'RE',
'REG',
'REGN',
'RF',
'RHI',
'RJF',
'RL',
'RMD',
'ROK',
'ROL',
'ROP',
'ROST',
'RSG',
'RTX',
'SBAC',
'SBUX',
'SCHW',
'SEDG',
'SEE',
'SHW',
'SJM',
'SLB',
'SNA',
'SNPS',
'SO',
'SPG',
'SPGI',
'SRE',
'STE',
'STLD',
'STT',
'STX',
'STZ',
'SWK',
'SWKS',
'SYF',
'SYK',
'SYY',
'T',
'TAP',
'TDG',
'TDY',
'TECH',
'TEL',
'TER',
'TFC',
'TFX',
'TGT',
'TJX',
'TMO',
'TMUS',
'TPR',
'TRGP',
'TRMB',
'TROW',
'TRV',
'TSCO',
'TSLA',
'TSN',
'TT',
'TTWO',
'TXN',
'TXT',
'TYL',
'UAL',
'UDR',
'UHS',
'ULTA',
'UNH',
'UNP',
'UPS',
'URI',
'USB',
'V',
'VFC',
'VICI',
'VLO',
'VMC',
'VRSK',
'VRSN',
'VRTX',
'VTR',
'VTRS',
'VZ',
'WAB',
'WAT',
'WBA',
'WBD',
'WDC',
'WEC',
'WELL',
'WFC',
'WHR',
'WM',
'WMB',
'WMT',
'WRB',
'WRK',
'WST',
'WTW',
'WY',
'WYNN',
'XEL',
'XOM',
'XRAY',
'XYL',
'YUM',
'ZBH',
'ZBRA',
'ZION',
'ZTS'
)


