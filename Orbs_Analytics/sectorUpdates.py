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

# list of all sector urls to scrape
sectors = ["https://www.cnbc.com/technology/", "https://www.cnbc.com/health-and-science/", "https://www.cnbc.com/energy/", 
"https://www.cnbc.com/aerospace-defense/", "https://www.cnbc.com/retail/", "https://www.cnbc.com/e-commerce/"]

# function to get headlines given a URL
def scrape(webURL):
	soup = bs(req.get(url).content, "html.parser")
	headlines = []
	for link in soup.find_all('a'):
		l = link.string
		if(str(type(l)) == "<class 'bs4.element.NavigableString'>" and len(l.strip()) > 35 and 
			not(l.strip().split()[0] == "Best" or l.strip().split()[0] == "Personal" or "Market Data Terms" in l)): #filtering out irrelevant navigable strings
				headlines.append(l.strip())
	return headlines

# dataframe w/ columns as URL(sector) and rows as headlines
df = pd.DataFrame()

for url in sectors:
	print("\n" + str(url) + "\n")
	temp = pd.DataFrame({url:scrape(url)})
	df = pd.concat([df, temp], ignore_index=False, axis=1)
	# for h in scrape(url):
	# 	print(h)

# print(df)

# export the dataframe to an Excel sheet
with pd.ExcelWriter('/Users/aarontsui/Desktop/ORBS/sectorUpdates.xlsx', engine='openpyxl', mode='w') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False)


# Sentiment Analysis
sen = SentimentIntensityAnalyzer()
print(df['https://www.cnbc.com/technology/'][2])
print(sen.polarity_scores("Microsoft stock hits record as leaders see $10 billion in annual A.I. revenue. Disney finance chief Christine McCarthy to step down as Iger reshapes company. Russian ransomware hacker accused of extorting millions from U.S. businesses. Tesla's U.S. electric vehicle market share to drop to 18% by 2026: BofA estimate. U.S. withdraws new charges in Sam Bankman-Fried case, punts them to 2024. Bitcoin briefly drops below $25,000, Tether's stablecoin falls under dollar peg. $5 billion fintech Zepz plans M&A, new digital wallet despite job cuts. Oracle hits record after 50% surge in 2023, defying tech struggles. Shell CEO says EV charging stations in China are hot, sees 'robust' oil demand. CalPERS to boost venture capital investments despite startup market turmoil. EU charges Google with anti-competitive practices in ad tech business. Nvidia-backed firm that turns text into A.I. avatars hits $1 billion valuation."))
