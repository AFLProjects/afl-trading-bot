# Libraries to download
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Project Files
from api.connect import *
from api.order import *
from api.tracking import *
from dft.dft import *
from dft.denoise import *
from analysis.analyse import *

# System libraries
import urllib.request
import time
import csv
import os

index = 1
markets = []
print('Fectching trending markets...')
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)
for i in range(9):
    time.sleep(1)
    try:
        url = f'https://finviz.com/screener.ashx?v=210&s=ta_p_tlsupport&r={index}'
        print(f'[\'url\' : \'{url}\']')
        with urllib.request.urlopen(url) as f:
            html = f.read().decode('utf-8')
            parse = (html.split('<!-- TS')[1]).split('TE -->')[0]
            for i, value in enumerate(parse.splitlines()):
                ticker = value.split('|')[0]
                if ticker:
                    markets.append(ticker)
            index += 12
    except:
        print('No more markets')
        break
print(f"Found {len(markets)} markets with an uptrend.")
print(markets)



while True:
    getCurrentPrice('AAPL')

#https://finviz.com/screener.ashx?v=210&s=ta_p_tlsupport&r=1