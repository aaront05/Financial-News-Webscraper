from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd
import nltk
import ssl
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import seaborn as sns
from textblob import TextBlob


# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()

djia_tickers = [
    'AAPL', 'AMGN', 'AXP', 'BA', 'CAT', 'CRM', 'CSCO', 'CVX', 'DIS', 'DOW',
    'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM',
    'MRK', 'MSFT', 'NKE', 'PG', 'TRV', 'UNH', 'V', 'VZ', 'WBA', 'WMT'
]



sp500 = "https://topforeignstocks.com/indices/components-of-the-sp-500-index/"
sp500_tickers = []
soup = bs(req.get(sp500).content, "html.parser")
for sym in soup.find_all(attrs={"rel": "noopener"}):
    sp500_tickers.append(sym.string.strip())

print(len(sp500_tickers))
# print(sp500_tickers)









    






