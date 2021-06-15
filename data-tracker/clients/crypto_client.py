import requests

class CryptoClient:
    CRYPTO_API_PATH = 'https://api.cryptowat.ch'
    DEFAULT_EXCHANGE = 'kraken'

    def __init__(self, exchange=DEFAULT_EXCHANGE):
        self.exchange = exchange

    def get_price(self, symbol):
        url = self.CRYPTO_API_PATH + '/markets/' + self.exchange + '/' + symbol + '/price'
        resp = requests.get(url)
        resp_json = resp.json()
        return resp_json['result']

    def get_pairs(self, limit_to_btc_pairs=True):
        url = self.CRYPTO_API_PATH + '/markets/' + self.exchange
        resp = requests.get(url)
        resp_json = resp.json()
        return resp_json['result']
