from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd
from langdetect import detect

# REUTERS
website_reuters = ["https://www.reuters.com/news/archive/americasMergersNews?view=page&page=1&pageSize=10", "https://www.reuters.com/news/archive/americasMergersNews?view=page&page=2&pageSize=10", 
"https://www.reuters.com/news/archive/americasMergersNews?view=page&page=3&pageSize=10", "https://www.reuters.com/news/archive/americasMergersNews?view=page&page=4&pageSize=10", 
"https://www.reuters.com/news/archive/americasMergersNews?view=page&page=5&pageSize=10"]

# dataframe w/ columns as URL and rows as headlines
df_reuters = pd.DataFrame()


def scrape_reuters(webURL):
    soup = bs(req.get(url).content, "html.parser")
    headlines_reuters = []
    dates_reuters = []
    for link in soup.find_all("h3", class_="story-title"):
        headlines_reuters.append(link.string.strip())
    for date in soup.find_all("span", class_="timestamp"):
        dates_reuters.append(date.string.strip())
    headlines_reuters = headlines_reuters[:-3]  # filter our irrelevant headlines
    for i in range (len(headlines_reuters)):
        headlines_reuters[i] = headlines_reuters[i] + " (" + dates_reuters[i] + ")"
    return headlines_reuters

for url in website_reuters:
    temp = pd.DataFrame({url:scrape_reuters(url)})
    df_reuters = pd.concat([df_reuters, temp], ignore_index=False, axis=1)


# FINANCIAL TIMES
website_ft = "https://www.ft.com/mergers-acquisitions"

# dataframe w/ columns as URL and rows as headlines
df_ft = pd.DataFrame()

soup = bs(req.get(website_ft).content, "html.parser")
headlines_ft = []
for link in soup.find_all("a", class_="js-teaser-heading-link"):
    headlines_ft.append(link.string.strip())
temp = pd.DataFrame({website_ft:headlines_ft})
df_ft = pd.concat([df_ft, temp], ignore_index=False, axis=1)


# BUSINESS WIRE
website_bw = ["https://www.businesswire.com/portal/site/home/template.PAGE/news/subject/?javax.portlet.tpst=08c2aa13f2fe3d4dc1b6751ae1de75dd&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_vnsId=31333&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_viewID=MY_PORTAL_VIEW&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_ndmHsc=v2*A1686394800000*DgroupByDate*M31333*N1000105&javax.portlet.begCacheTok=com.vignette.cachetoken&javax.portlet.endCacheTok=com.vignette.cachetoken",
"https://www.businesswire.com/portal/site/home/template.PAGE/news/subject/?javax.portlet.tpst=08c2aa13f2fe3d4dc1b6751ae1de75dd&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_vnsId=31333&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_viewID=MY_PORTAL_VIEW&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_ndmHsc=v2*A1686394800000*B1689018795575*DgroupByDate*G2*M31333*N1000105&javax.portlet.begCacheTok=com.vignette.cachetoken&javax.portlet.endCacheTok=com.vignette.cachetoken", 
"https://www.businesswire.com/portal/site/home/template.PAGE/news/subject/?javax.portlet.tpst=08c2aa13f2fe3d4dc1b6751ae1de75dd&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_vnsId=31333&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_viewID=MY_PORTAL_VIEW&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_ndmHsc=v2*A1686394800000*B1689018855316*DgroupByDate*G3*M31333*N1000105&javax.portlet.begCacheTok=com.vignette.cachetoken&javax.portlet.endCacheTok=com.vignette.cachetoken", 
"https://www.businesswire.com/portal/site/home/template.PAGE/news/subject/?javax.portlet.tpst=08c2aa13f2fe3d4dc1b6751ae1de75dd&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_vnsId=31333&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_viewID=MY_PORTAL_VIEW&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_ndmHsc=v2*A1686394800000*B1689018884690*DgroupByDate*G4*M31333*N1000105&javax.portlet.begCacheTok=com.vignette.cachetoken&javax.portlet.endCacheTok=com.vignette.cachetoken", 
"https://www.businesswire.com/portal/site/home/template.PAGE/news/subject/?javax.portlet.tpst=08c2aa13f2fe3d4dc1b6751ae1de75dd&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_vnsId=31333&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_viewID=MY_PORTAL_VIEW&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_ndmHsc=v2*A1686394800000*B1689018924887*DgroupByDate*G5*M31333*N1000105&javax.portlet.begCacheTok=com.vignette.cachetoken&javax.portlet.endCacheTok=com.vignette.cachetoken"]

# dataframe w/ columns as URL and rows as headlines
df_bw = pd.DataFrame()

def scrape_bw(webURL):
    soup = bs(req.get(url).content, "html.parser")
    headlines_bw = []
    dates_bw = []
    for link in soup.find_all(attrs={"itemprop": "headline"}):
        headlines_bw.append(link.string.strip())
    for date in soup.find_all(attrs={"itemprop": "dateModified"}):
        dates_bw.append(date.string.strip())
    for i in range (len(headlines_bw)):
        headlines_bw[i] = headlines_bw[i] + " (" + dates_bw[i] + ")"
    return headlines_bw

n = 1
for url in website_bw:
    headlines = scrape_bw(url)
    headlines = [t for t in headlines if detect(t) == 'en'] # filter out all non-english headlines
    page_num = "Business Wire M&A Page " + str(n)
    n += 1
    temp = pd.DataFrame({page_num:headlines})
    df_bw = pd.concat([df_bw, temp], ignore_index=False, axis=1)


# PRINT DATAFRAMES FOR INSPECTION 
print(df_reuters)
print(df_ft)
print(df_bw)


# EXPORT TO EXCEL SHEETS
with pd.ExcelWriter('/Users/aarontsui/Desktop/ORBS/m&a_reuters.xlsx', engine='openpyxl', mode='w') as writer:
    df_reuters.to_excel(writer, sheet_name='Sheet1', index=False)

with pd.ExcelWriter('/Users/aarontsui/Desktop/ORBS/m&a_ft.xlsx', engine='openpyxl', mode='w') as writer:
    df_ft.to_excel(writer, sheet_name='Sheet1', index=False)

with pd.ExcelWriter('/Users/aarontsui/Desktop/ORBS/m&a_bw.xlsx', engine='openpyxl', mode='w') as writer:
    df_bw.to_excel(writer, sheet_name='Sheet1', index=False)

# finished
print("SUCCESSFULLY EXECUTED SCRIPT")