from flask import Flask, Response
import json

from application_services.StocksResource.stocks_resource import StocksResource
import database_services.RDBService as d_service

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/stocks/update_all')
def update_stocks():  # put application's code here
    res = StocksResource.update_stocks()
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


@app.route('/stocks/<prefix>')
def get_stock(prefix):  # put application's code here
    res = StocksResource.get_by_ticker_prefix(prefix)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


@app.route('/stocks')
def get_all_stocks():
    res = StocksResource.get_stocks_table()
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


@app.route('/stocks/clear_all')
def clear_all_stocks():
    res = StocksResource.clear_stocks_table()
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


@app.route('/stocks/<prefix>/delete')
def delete_stock(prefix):  # put application's code here
    res = StocksResource.delete_by_ticker_prefix(prefix)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


if __name__ == '__main__':
    app.run()
