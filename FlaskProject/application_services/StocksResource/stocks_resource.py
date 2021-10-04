import numpy as np
import pandas as pd
import requests

from application_services.BaseApplicationResource import BaseApplicationResource
from secrets import IEX_CLOUD_API_TOKEN

class StocksResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    def chunks(lst, n):
        """Yield successive n-sized chunks from lst"""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    @classmethod
    def get_stocks(cls):
        stocks = pd.read_csv('sp_500_stocks.csv')
        symbol_groups = list(cls.chunks(stocks['Ticker'], 100))
        symbol_strings = []
        for i in range(0, len(symbol_groups)):
            symbol_strings.append(','.join(symbol_groups[i]))
        for symbol_string in symbol_strings:
            batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=company,quote&token={IEX_CLOUD_API_TOKEN}'
            data = requests.get(batch_api_call_url).json()
            for symbol in symbol_string.split(','):
                print(data[symbol]['company']['companyName'],symbol,data[symbol]['quote']['latestPrice'])
        return 1
