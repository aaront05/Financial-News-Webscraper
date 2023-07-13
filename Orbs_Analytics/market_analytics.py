from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd
import nltk
import ssl
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import seaborn as sns
from textblob import TextBlob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()

current_date = datetime.datetime.now().date()
current_time = datetime.datetime.now().time()

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

# print(len(sp500_tickers))
# print(sp500_tickers)

nasdaq = "https://www.slickcharts.com/nasdaq100"
nasdaq_tickers = []
chrome_options = Options()
chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(options=chrome_options)
driver.get(nasdaq)
page_source = driver.page_source
soup = bs(page_source, "html.parser")
driver.quit()
for ticker in soup.find_all('a', href=lambda href: href and 'symbol' in href):
    if len(ticker.text.strip()) <= 5:
        nasdaq_tickers.append(ticker.text.strip())



# filter out non-nasdaq symbols on page
nasdaq_tickers = nasdaq_tickers[:-4]

# print(nasdaq_tickers)
# print(len(nasdaq_tickers))

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


# PREVIOUS VERISON - SINGLE HEADLINES INDIVIDUALLY ANALYZED, THEN ALL SCORES COMBINED, THEN SCORES AVERAGED)

# def scrape(ticker_list):
#     headlines_combined = []
#     for t in ticker_list:
#         soup = bs(req.get(sources[0] + t).content, "html.parser")
#         for headline in soup.find_all("h4", class_="article__title-text"):
#             headlines_combined.append(headline.string)

#         soup = bs(req.get(sources[1] + t).content, "html.parser")
#         for headline in soup.find_all('a'):
#             h = headline.string
#             if(str(type(h)) == "<class 'bs4.element.NavigableString'>" and len(h.strip()) > 35):
#                 headlines_combined.append(h.strip())
        
#         headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#         }   
#         response = req.get((sources[2] + t), headers=headers)
#         soup = bs(response.content, "html.parser")
#         for headline in soup.find_all('a'):
#             h = headline.string
#             if(str(type(h)) == "<class 'bs4.element.NavigableString'>" and len(h.strip()) > 35):
#                 headlines_combined.append(h.strip())
#     return headlines_combined

# def sentiment(headlines):
#     count, combined_polarity, combined_subjectivity, combined_neg, combined_neu, combined_pos, combined_compound = 0
#     for headline in headlines:
#         sen = SentimentIntensityAnalyzer()
#         dict = sen.polarity_scores(headline)
#         combined_neg += dict['neg']
#         combined_neu += dict['neu']
#         combined_pos += dict['pos']
#         combined_compound += dict['compound']
#         blob = TextBlob(headline)
#         polarity = blob.sentiment.polarity
#         subjectivity = blob.sentiment.subjectivity
#         count += 1
#         combined_polarity += polarity
#         combined_subjectivity += subjectivity
#     print("TextBlob Polarity = " + str(combined_polarity/count))
#     print("TextBlob Subjectivity = " + str(combined_subjectivity/count))
#     print("VADER neg/neu/pos = " + str(combined_neg/count) + "/" + + str(combined_neu/count) + "/" + + str(combined_pos/count))
#     print("VADER compound = " + str(combined_compound/count))
#     return [combined_polarity/count, combined_subjectivity/count, combined_neg/count, combined_neu/count, combined_pos/count, combined_compound/count]


# CURRENT VERSION - Sentiment Analysis on EACH INDIVIDUAL TICKER, THEN FOR EACH INDEX
def scrape_ticker(ticker):
    ticker_headlines = []
    soup = bs(req.get(sources[0] + ticker).content, "html.parser")
    for headline in soup.find_all("h4", class_="article__title-text"):
        ticker_headlines.append(headline.string)

    soup = bs(req.get(sources[1] + ticker).content, "html.parser")
    for headline in soup.find_all('a'):
        h = headline.string
        if(str(type(h)) == "<class 'bs4.element.NavigableString'>" and len(h.strip()) > 35):
            ticker_headlines.append(h.strip())
    
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }   
    response = req.get((sources[2] + ticker), headers=headers)
    soup = bs(response.content, "html.parser")
    for headline in soup.find_all('a'):
        h = headline.string
        if(str(type(h)) == "<class 'bs4.element.NavigableString'>" and len(h.strip()) > 35):
            ticker_headlines.append(h.strip())
    return ticker_headlines

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
    print("TextBlob Polarity = " + str(((combined_polarity/count) + 1)*50))
    print("TextBlob Subjectivity = " + str(((combined_subjectivity/count) + 1) * 50))
    print("VADER neg/neu/pos = " + str(((combined_neg/count) + 1) * 50) + "/" + str(((combined_neu/count) + 1) * 50) + "/" + str(((combined_pos/count) + 1) * 50))
    print("VADER compound = " + str(((combined_compound/count) + 1) * 50))
    return [combined_polarity/count, combined_subjectivity/count, combined_neg/count, combined_neu/count, combined_pos/count, combined_compound/count]

def sentiment_ticker(index_list):
    index_polarity = 0
    index_subjectivity = 0
    index_neg = 0
    index_neu = 0
    index_pos = 0
    index_compound = 0
    count = 0
    for ticker in index_list:
        count += 1
        ticker_headlines = scrape_ticker(ticker)
        print("\nStock: " + ticker)
        sentiment_list = sentiment(ticker_headlines)
        index_polarity += sentiment_list[0]
        index_subjectivity += sentiment_list[1]
        index_neg += sentiment_list[2]
        index_neu += sentiment_list[3]
        index_pos += sentiment_list[4]
        index_compound += sentiment_list[5]
    print("\nINDEX TEXTBLOB POLARITY: " + str(((index_polarity/count)+ 1)*50))
    print("INDEX TEXTBLOB POLARITY: " + str(((index_subjectivity/count)+ 1)*50))
    print("INDEX VADER NEG/NEU/POS: " + str(((index_neg/count)+ 1)*50) + "/" + str(((index_neu/count)+ 1)*50) + "/" + str(((index_pos/count)+ 1)*50))
    print("INDEX VADER COMPOUND: " + str(((index_compound/count)+ 1)*50))
    
print("Current Date:", current_date)
print("Current Time:", current_time)
print("\nSentiment Analysis on Individual Stocks in DJIA: ")
sentiment_ticker(djia_tickers)
print("\nSentiment Analysis on Individual Stocks in S&P 500: ")
sentiment_ticker(sp500_tickers)
print("\nSentiment Analysis on Individual Stocks in Nasdaq-100: ")
sentiment_ticker(nasdaq_tickers)
print("Success - Program Complete")
        
        










    






