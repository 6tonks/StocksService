import numpy as np
import pandas as pd
import requests

from application_services.BaseApplicationResource import BaseApplicationResource
from secrets import IEX_CLOUD_API_TOKEN

class StocksResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_stocks(cls):
        stocks = pd.read_csv('sp_500_stocks.csv')
        symbol = 'AAPL'
        api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}'
        data = requests.get(api_url).json()
        print(data)
        return 1
