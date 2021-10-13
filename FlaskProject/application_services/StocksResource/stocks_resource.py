import numpy as np
import pandas as pd
import requests

from application_services.BaseApplicationResource import BaseApplicationResource
from secrets import IEX_CLOUD_API_TOKEN
import database_services.RDBService as d_service


class StocksResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    def chunks(lst, n):
        """Yield successive n-sized chunks from lst"""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    @classmethod
    def update_stocks(cls):
        stocks = pd.read_csv('sp_500_stocks.csv')
        symbol_groups = list(cls.chunks(stocks['Ticker'], 100))
        symbol_strings = []
        for i in range(0, len(symbol_groups)):
            symbol_strings.append(','.join(symbol_groups[i]))
        for symbol_string in symbol_strings:
            batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=company,quote&token={IEX_CLOUD_API_TOKEN}'
            data = requests.get(batch_api_call_url).json()
            for symbol in symbol_string.split(','):
                company_name = data[symbol]['company']['companyName']
                latest_price = data[symbol]['quote']['latestPrice']
                res = d_service.update_stock("stocksresource", "stocks",
                                                       symbol, company_name, latest_price)
        return res

    @classmethod
    def get_table(cls, name_prefix):
        res = d_service.get_table("stocksresource", "stocks")
        return res
