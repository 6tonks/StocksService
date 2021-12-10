from flask import Flask, Response, request
import json

from application_services.StocksResource.stocks_resource import StocksResource
import database_services.RDBService as d_service

app = Flask(__name__)


@app.route('/', methods=['GET'])
def welcome():
    return {"Welcome": 'Stocks Service',
            "links": [
                {
                    'rel': 'Get all stocks info',
                    'method': 'GET',
                    'href': '/api/stocks'
                },
                {
                    'rel': 'Trigger stock table update from IEX Cloud',
                    'method': 'GET',
                    'href': '/api/stocks/update_all'
                },
                {
                    'rel': 'Get stock info',
                    'method': 'GET',
                    'href': '/api/stocks/<ticker>'
                },
                {
                    'rel': 'Delete stock from stocks table',
                    'method': 'DELETE',
                    'href': '/api/stocks/<prefix>'
                },
                {
                    'rel': 'Clear stocks table',
                    'method': 'DELETE',
                    'href': '/api/stocks/clear_all'
                }
            ]
            }

@app.route('/api/stocks/update_all', methods=['GET'])
def update_stocks():  # put application's code here
    res, status = StocksResource.update_stocks()
    if status == 200:
        res = {"links": [
                    {
                        'rel': 'all stocks',
                        'href': '/api/stocks'
                    },
                    {
                        'rel': 'single stock',
                        'href': '/api/stocks/<ticker>'
                    }
                ]
               }
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


@app.route('/api/stocks/<ticker>', methods=['GET', 'DELETE'])
def single_stock_route(ticker):  # put application's code here
    if request.method == 'GET':
        res, status = StocksResource.get_by_ticker_prefix(ticker)
        if status == 200:
            res["self"] = f'/api/stocks/{ticker}'
            res["links"] = [
                {
                    'rel': 'all stocks',
                    'href': '/api/stocks/'
                }
            ]
    elif request.method == 'DELETE':
        res, status = StocksResource.delete_by_ticker_prefix(ticker)
        if status == 200:
            res = {"links": [
                                {
                                    'rel': 'all stocks',
                                    'href': '/api/stocks/'
                                },
                                {
                                    'rel': 'Trigger stock table update from IEX Cloud',
                                    'href': '/api/stocks/update_all'
                                }
                            ]
                   }
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


@app.route('/api/stocks', methods=['GET'])
def get_all_stocks():
    res = {}
    res["stocks"], status = StocksResource.get_stocks_table()
    if status == 200:
        if len(res["stocks"]) > 0:
            res["self"] = '/api/stocks'
            res["links"] = [
                {
                    'rel': 'single stock',
                    'href': '/api/stocks/<ticker>'
                }
            ]
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


@app.route('/api/stocks/clear_all', methods=['DELETE'])
def clear_all_stocks():
    res, status = StocksResource.clear_stocks_table()
    if status == 200:
        res = {"links": [
            {
                'rel': 'Trigger stock table update from IEX Cloud',
                'href': '/api/stocks/update_all'
            }
        ]
        }
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


if __name__ == '__main__':
    app.run()
