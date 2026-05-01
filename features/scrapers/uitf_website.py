import requests
from bs4 import BeautifulSoup
import csv

from os import makedirs
from time import sleep
import re
from datetime import datetime
from collections import deque

from features.common.uitf_web_keys import BANK_ID_MAPPING

def extract_time(dt_str):
    date_obj = datetime.strptime(dt_str.strip(), "%b %d, %Y")
    return date_obj.strftime("%Y-%m-%d")

def extract_row_values(tr, dt_default : str):
    fund_name, fund_value = [td.get_text(strip=True) for td in tr.find_all('td')[:2]]
    fund_name = fund_name.title().replace(" ", "_")

    if "as of" in fund_value:
        fund_value , dt_str = fund_value.split("* as of ")
        dt_row = extract_time(dt_str.strip())

    else:
        dt_row = dt_default

    fund_value = float(fund_value.replace(",", ""))
    
    return fund_name , [dt_row, fund_value]



def extract(bank_name : str, bank_id : int):
    OUTPUT_FOLDER = f"data/navpu/{bank_name}"
    URL = f'https://uitf.com.ph/daily_navpu.php?bank_id={bank_id}'

    makedirs(OUTPUT_FOLDER, exist_ok=True)

    # SCRAPE
    response = requests.get(URL)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, 'html.parser')

    # DATE
    dt_str = soup.find('h2').get_text(strip=True)
    dt_match = re.search(r'([A-Za-z]{3} \d{1,2}, \d{4})', dt_str)
    
    # dt_header = datetime.strftime(dt_str, '%b %d, %Y')
    dt_header = extract_time(dt_str=dt_match.group(1))


    
    # FUNDS
    start = soup.find(class_="table-title mt-5")

    for tb in start.find_all_next('tbody'):
        for tr in tb.find_all('tr'):
            try:
                fund_name , new_row = extract_row_values(tr=tr, dt_default=dt_header)
            
                file_path = f"{OUTPUT_FOLDER}/{fund_name}.csv"

                with open(file_path, 'r', newline='') as f:
                    last_row = list(csv.reader(f))[-1]
                
                if last_row[0] != new_row[0]:
                    with open(f"{OUTPUT_FOLDER}/{fund_name}.csv", 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(new_row)
                    
                    print(f'{fund_name}: {new_row[1]}')
            
            
            except Exception as e:
                print(f"[ERROR] : {e}")
                continue

            

if __name__ == "__main__":
    for bank_name, bank_id in BANK_ID_MAPPING.items():
        print(bank_name)
        extract(bank_name, bank_id)
        sleep(1)