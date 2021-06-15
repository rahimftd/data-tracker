from .handlers.handlers import Handler
from .clients.crypto_client import CryptoClient
from .dal.dal import CryptoDAL
from flask import Flask, request

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    dal = CryptoDAL()
    crypto_client = CryptoClient()
    handler = Handler(crypto_client, dal)

    @app.route('/currency-dropdown', methods=['GET'])
    def get_currency_dropdown():
        return handler.handle_get_currency_dropdown()

    @app.route('/price-l24h/<symbol>', methods=['GET'])
    def get_price_l24h(symbol):
        return handler.handle_get_price_l24h(symbol)

    @app.route('/rank', methods=['POST'])
    def post_ranking():
        symbols = request.json.get('symbols', None)
        if symbols is None:
            raise Exception("symbols cannot be none")
        return handler.handle_post_rank(symbols)

    return app
