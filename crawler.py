import requests
from bs4 import BeautifulSoup

from datetime import datetime

symbol = 'AAPL'
URL = 'https://www.stocksplithistory.com/?symbol=' + symbol
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'lxml')

table = soup.find("table", width=208, style="font-family: Arial; font-size: 12px")

rows = table.find_all('tr')

split_dates = []
split_ratio = []

if len(rows) > 1:
    for row in rows[1:]:
        tds = row.findChilden('td')
        split_date = datetime.strptime(tds[0].text, '%m/%d/%Y')

        if split_date >= datetime.strptime('01/03/2007', '%m/%d/%Y'):
            split_dates.append(str(split_date.year) + str(split_date.month) + str(split_date.day))
            ratio_text = list(tds[1].text.strip('\n'))
            ratio = int(ratio_text[0]) / int(ratio_text[1])
            split_ratio.append(ratio)

