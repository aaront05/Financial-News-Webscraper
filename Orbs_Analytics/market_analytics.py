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

sources = ["https://site.financialmodelingprep.com/financial-summary/", "https://research.tdameritrade.com/grid/public/research/stocks/news/search?symbol=", "https://finviz.com/quote.ashx?t="]

# def scrape(t):
#     output = ""

#     soup = bs(req.get(sources[0] + t).content, "html.parser")
#     for headline in soup.find_all("h4", class_="article__title-text"):
#         output += headline.string + "." + "\n"

#     soup = bs(req.get(sources[1] + t).content, "html.parser")
#     for headline in soup.find_all('a'):
#         h = headline.string
#         if(str(type(h)) == "<class 'bs4.element.NavigableString'>" and len(h.strip()) > 35):
#             output += h.strip() + "." + "\n"
    
#     headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#     }   
#     response = req.get((sources[2] + t), headers=headers)
#     soup = bs(response.content, "html.parser")
#     for headline in soup.find_all('a'):
#         h = headline.string
#         if(str(type(h)) == "<class 'bs4.element.NavigableString'>" and len(h.strip()) > 35):
#             output += h.strip() + "." + "\n"

#     return output

# ALL HEADLINES GROUPED INTO ONE STRING, THEN ANALYZED

# def sentiment(ticker_list):
#     text_to_analyze = ""
#     for ticker in ticker_list:
#         t = scrape(ticker)
#         text_to_analyze += t + ". "
#     blob = TextBlob(t)
#     polarity = blob.sentiment.polarity
#     subjectivity = blob.sentiment.subjectivity
#     sen = SentimentIntensityAnalyzer()
#     print(sen.polarity_scores(text_to_analyze))
#     print(polarity)
#     print(subjectivity)

# sentiment(djia_tickers)

# TEXT GROUPED BY STOCK, ANALYZED, COMBINED, THEN AVERAGED

# def sentiment_2(ticker_list):
#     count = 0
#     combined_polarity = 0
#     combined_subjectivity = 0
#     for ticker in ticker_list:
#         t = scrape(ticker)
#         blob = TextBlob(t)
#         sen = SentimentIntensityAnalyzer()
#         print(sen.polarity_scores(t))
#         polarity = blob.sentiment.polarity
#         subjectivity = blob.sentiment.subjectivity
#         count += 1
#         combined_polarity += polarity
#         combined_subjectivity += subjectivity
#     print(combined_polarity/count)
#     print(combined_subjectivity/count)

# sentiment_2(djia_tickers)


# CURRENT VERISON (SINGLE HEADLINES INDIVIDUALLY ANALYZED, THEN ALL SCORES COMBINED, THEN SCORES AVERAGED)

def scrape(ticker_list):
    headlines_combined = []
    for t in ticker_list:
        soup = bs(req.get(sources[0] + t).content, "html.parser")
        for headline in soup.find_all("h4", class_="article__title-text"):
            headlines_combined.append(headline.string)

        soup = bs(req.get(sources[1] + t).content, "html.parser")
        for headline in soup.find_all('a'):
            h = headline.string
            if(str(type(h)) == "<class 'bs4.element.NavigableString'>" and len(h.strip()) > 35):
                headlines_combined.append(h.strip())
        
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        }   
        response = req.get((sources[2] + t), headers=headers)
        soup = bs(response.content, "html.parser")
        for headline in soup.find_all('a'):
            h = headline.string
            if(str(type(h)) == "<class 'bs4.element.NavigableString'>" and len(h.strip()) > 35):
                headlines_combined.append(h.strip())
    return headlines_combined

def sentiment(headlines):
    count = 0
    combined_polarity = 0
    combined_subjectivity = 0
    combined_neg = 0
    combined_neu = 0
    combined_pos = 0
    combined_compound = 0
    for headline in headlines:
        sen = SentimentIntensityAnalyzer()
        dict = sen.polarity_scores(headline)
        combined_neg += dict['neg']
        combined_neu += dict['neu']
        combined_pos += dict['pos']
        combined_compound += dict['compound']
        blob = TextBlob(headline)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        count += 1
        combined_polarity += polarity
        combined_subjectivity += subjectivity
    print("TextBlob Polarity = " + str(combined_polarity/count))
    print("TextBlob Subjectivity = " + str(combined_subjectivity/count))
    print("VADER neg = " + str(combined_neg/count))
    print("VADER neu = " + str(combined_neu/count))
    print("VADER pos = " + str(combined_pos/count))
    print("VADER compound = " + str(combined_compound/count))


sentiment(scrape(djia_tickers))
sentiment(scrape(sp500_tickers))




        










    






