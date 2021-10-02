from flask import Flask

from application_services.StocksResource.stocks_resource import StocksResource

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here

    return 'Hello World!'
StocksResource.get_stocks()

if __name__ == '__main__':
    app.run()
