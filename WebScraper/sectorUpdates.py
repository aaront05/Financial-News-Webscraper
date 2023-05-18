from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd

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
	for h in scrape(url):
		print(h)

print(df)

# export the dataframe to an Excel sheet
with pd.ExcelWriter('/Users/aarontsui/Desktop/ORBS/sectorUpdates.xlsx', engine='openpyxl', mode='w') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False)