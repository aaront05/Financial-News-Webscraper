from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd
import seaborn as sns

import requests

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1318&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=DFF&scale=left&cosd=1954-07-01&coed=1959-07-16&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily%2C%207-Day&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2023-06-15&revision_date=2023-06-15&nd=1954-07-01"

response = requests.get(url)

if response.status_code == 200:
    with open("c.csv", "wb") as file:
        file.write(response.content)
    print("Download successful.")
else:
    print("Download failed")



