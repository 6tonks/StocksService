from flask import Flask, Response
import json

from application_services.StocksResource.stocks_resource import StocksResource
import database_services.RDBService as d_service

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/update_stocks')
def update_stocks():  # put application's code here
    res = StocksResource.update_stocks()
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp

@app.route('/users')
def get_users():
    res = StocksResource.get_table(None)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


if __name__ == '__main__':
    app.run()
