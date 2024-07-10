from io import StringIO
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
from datetime import datetime

def log_progress(message):
    '''This function records a specific message about the current step of the program into a log file and doesn't return any value.'''
    with open('./code_log.txt','w') as f:
        f.write(f'{datetime.now()}: {message}\n')

def extract(url, table_attribs):
    '''Extracts the data from the website and save it to a dataframe.'''
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    table = soup.find('span', string = table_attribs).find_next('table')
    df = pd.read_html(StringIO(str(table)))[0]
    log_progress('Data extraction')
    return df

def transform(df, csv_path):
    '''this function accesses the CSV file for exchange rate information,
    and adds three more columns for the dataframe, each containing the transformed
    version of market cap column to resprective currencies'''
    exchange_rate = pd.read_csv(csv_path, index_col = 0).to_dict()['Rate']
    print(exchange_rate)
    df['GBP_Billion'] = round(df['Market cap (US$ billion)'] *exchange_rate['GBP'], 2)
    df['EUR_Billion'] = round(df['Market cap (US$ billion)'] *exchange_rate['EUR'], 2)
    df['INR_Billion'] = round(df['Market cap (US$ billion)'] *exchange_rate['INR'], 2)
    log_progress('Data transformation')
    return df

def load_to_db(df, sql_connection, table_name):
    '''This function saves the final dataframe to a database table with the provided name'''
    df.to_sql(table_name, sql_connection, if_exists = 'replace', index = False)
    log_progress('Data Loaded to Database as a table, Executing quries')

def load_to_csv(df, output_path):
    '''This function saves the final dataframe as a CSV file in the provided path'''
    df.to_csv(output_path)
    log_progress('Data Save to the CSV file')


def run_query(query_statement, sql_connection):
    '''This function runs the query on the database table and prints the output on the terminal'''
    cursor = sql_connection.cursor()
    cursor.execute(query_statement)
    result = cursor.fetchall()
    log_progress('Process Complete')
    return result

if __name__ == '__main__':
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.width', None)        # Do not limit the display width
    url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
    output_csv_path = './output/Largest_banks_data.csv'
    database_name = './output/Banks.db'
    table_name = 'Largest_banks'
    log_progress('Preliminaries complete. Initiating ETL process')
    df = extract(url, 'By market capitalization')
    print("Orignal DataFrame From the Website: ")
    print(df.head()) 
    log_progress('Extraction Completed')

    df = transform(df, './input/exchange_rate.csv')
    log_progress('Data Transformed Successfully')
    print("Transformed Data Columns after Extra currencies: ")
    print(df.head())
    load_to_csv(df, output_csv_path)

    with sqlite3.connect(database_name) as conn:
        load_to_db(df, conn, table_name)

        run_query('SELECT * FROM Largest_banks', conn)

        run_query('SELECT AVG(GBP_Billion) FROM Largest_banks', conn)

        run_query('SELECT "Bank name" FROM Largest_banks LIMIT 5', conn)