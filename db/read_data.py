import sqlite3
import pandas as pd
import requests
from io import StringIO

connection = sqlite3.connect("data.db")
csv_url = 'https://data.montreal.ca/dataset/49ff9fe4-eb30-4c1a-a30a-fca82d4f5c2f/resource/6173de60-c2da-4d63-bc75-0607cb8dcb74/download/declarations-exterminations-punaises-de-lit.csv'
s=requests.get(csv_url).text
df = pd.read_csv(StringIO(s))
df.to_sql('data', con=connection, if_exists='append', index=False)


