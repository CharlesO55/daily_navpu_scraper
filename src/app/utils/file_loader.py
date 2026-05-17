from pathlib import Path
import pandas as pd

navpu_folder = Path("data/navpu")


def get_bank_uitf_funds_list():
    bank_funds_list = {}
    
    for bank_folder in navpu_folder.iterdir():
        bank_funds_list[bank_folder.name] = []

        for fund_file in bank_folder.glob("*.csv"):
            fund_data = {
                "name": fund_file.stem.replace("_", " "),
                "path": fund_file
            }
            
            bank_funds_list[bank_folder.name].append(fund_data)

    return bank_funds_list



def build_df_from_uitf_funds(selected_funds):
    df_list = []
                
    for fund in selected_funds:
        path = fund.get("path")

        temp_df = pd.read_csv(path, 
            header=0, 
            parse_dates=['date'], 
        ).dropna().drop_duplicates()

        temp_df['date'] = temp_df['date'].dt.date
        temp_df['fund_name'] = fund.get('name')

        df_list.append(temp_df)


    df_master = pd.concat(df_list)
    df_master.sort_values(['fund_name', 'date'], inplace=True)
    del df_list , temp_df

    return df_master