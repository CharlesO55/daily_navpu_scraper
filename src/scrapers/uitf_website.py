import requests
from bs4 import BeautifulSoup
import csv

from os import makedirs
from os.path import exists
from time import sleep
import re
import math
from datetime import datetime
from collections import deque

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

from src.common.uitf_web_keys import BANK_ID_MAPPING

def extract_time(dt_str):
    date_obj = datetime.strptime(dt_str.strip(), "%b %d, %Y")
    return date_obj.strftime("%Y-%m-%d")

def extract_row_text(tr):
    '''
    Extract str values from the table:
    
    +------------+-------+
    | Fund Name  | Navpu |
    +------------+-------+
    '''
    tds = tr.find_all('td')
    if len(tds) < 2:
        return None, None

    fund_name, fund_value = [td.get_text(strip=True) for td in tds[:2]]
    fund_name = fund_name.title().replace(" ", "_")

    return fund_name, fund_value


def extract_row_values(tr, dt_default : str):
    fund_name, fund_value = extract_row_text(tr)
    if not fund_name or not fund_value:
        # Row has no usable cells (e.g. header/spacer row) — silent skip
        return None
    
    raw_value = fund_value  # preserve original text before any mutation

    if "as of" in fund_value:
        try:
            fund_value, dt_str = fund_value.split("* as of ")
            fund_dt = extract_time(dt_str.strip())
        except Exception:
            raise ValueError(f"Could not parse 'as of' date from: {raw_value!r}")
    else:
        fund_dt = dt_default

    # Value guard: verify scraped navpu value is a float, else raise
    try:
        clean_value = fund_value.replace(",", "").strip()
        navpu_float = float(clean_value)
    except (ValueError, TypeError):
        raise ValueError(f"Not a float: {raw_value!r}")

    if navpu_float <= 0 or math.isnan(navpu_float) or math.isinf(navpu_float):
        raise ValueError(f"Invalid navpu value: {raw_value!r} → {navpu_float}")

    return fund_name, [fund_dt, navpu_float]



def extract(bank_name : str, bank_id : int):
    OUTPUT_FOLDER = f"data/navpu/{bank_name}"
    URL = f'https://uitf.com.ph/daily_navpu.php?bank_id={bank_id}'

    makedirs(OUTPUT_FOLDER, exist_ok=True)

    # SCRAPE
    response = requests.get(URL)
    if response.status_code != 200:
        raise RuntimeError(f"HTTP {response.status_code} for {URL}")
    soup = BeautifulSoup(response.content, 'html.parser')

    # DATE
    dt_str = soup.find('h2').get_text(strip=True)
    dt_match = re.search(r'([A-Za-z]{3} \d{1,2}, \d{4})', dt_str)
    if not dt_match:
        raise ValueError(f"Could not parse date from page header: {dt_str!r}")
    dt_header = extract_time(dt_str=dt_match.group(1))

    # FUNDS
    start = soup.find(class_="table-title mt-5")
    if not start:
        raise ValueError(f"Could not find fund table on page for bank_id={bank_id}")

    for tb in start.find_all_next('tbody'):
        for tr in tb.find_all('tr'):
            try:
                row_data = extract_row_values(tr=tr, dt_default=dt_header)
                if not row_data:
                    continue

                fund_name, new_row = row_data

                logging.info(fund_name)

                file_path = f"{OUTPUT_FOLDER}/{fund_name}.csv"

                # Create new file
                if not exists(file_path):
                    with open(file_path, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['date', 'value'])
                        writer.writerow(new_row)
                # Append only if date not already recorded
                else:
                    with open(file_path, 'r', newline='') as f:
                        rows = deque(csv.reader(f), maxlen=1)
                        last_row = rows[0] if rows else None

                    if last_row is None or last_row[0] != new_row[0]:
                        with open(file_path, 'a', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(new_row)

            
            except Exception as e:
                logging.exception(e)
                try:
                    fund_name, raw_value = extract_row_text(tr=tr)
                    error_path = 'data/scrape_errors.csv'
                    write_header = not exists(error_path)
                    with open(error_path, 'a', newline='') as f:
                        writer = csv.writer(f)
                        if write_header:
                            writer.writerow(['fund_name', 'date', 'raw_value'])
                        writer.writerow([
                            fund_name or 'unknown',
                            dt_header,
                            raw_value or '',
                        ])
                except Exception:
                    pass

                continue






if __name__ == "__main__":
    fail_cases = []

    for bank_name, bank_id in BANK_ID_MAPPING.items():
        logging.info("Processing %s", bank_name)
        
        try:
            extract(bank_name, bank_id)
        except Exception as e:
            logging.exception(e)
            fail_cases.append(bank_name)
        sleep(2)

    if fail_cases:
        logging.error("Broken Bank Pages: %s", fail_cases)
        # sys.exit(1)  # Fail the CI/CD job