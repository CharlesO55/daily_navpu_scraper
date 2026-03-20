import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv

import re


OUTPUT_FOLDER = "data/chinabank"
URL = 'https://uitf.com.ph/daily_navpu.php?bank_id=7'

response = requests.get(URL)

assert response.status_code == 200

soup = BeautifulSoup(response.content, 'html.parser')


# DATE
dt_str = soup.find('h2').get_text(strip=True)
match = re.search(r'([A-Za-z]{3} \d{1,2}, \d{4})', dt_str)
dt_str = match.group(1)

dt = datetime.strptime(dt_str, '%b %d, %Y').date()


# FUNDS
start = soup.find(class_="table-title mt-5")

for tb in start.find_all_next('tbody'):
    for tr in tb.find_all('tr'):
        fund_name, fund_value = [td.get_text(strip=True) for td in tr.find_all('td')[:2]]
        fund_name = fund_name.title().replace(" ", "_")

        with open(f"{OUTPUT_FOLDER}/{fund_name}.csv", 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([dt, fund_value])
        
        # print(f'{fund_name}: {fund_value}')