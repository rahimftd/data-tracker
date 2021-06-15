import sched, time

s = sched.scheduler(time.time, time.sleep)

DEFAULT_QUERY_INTERVAL = 60
DEFAULT_SYMBOLS = [
    {'pair': 'btceur'},
    {'pair': 'btcusd'},
    {'pair': 'btcgbp'},
    {'pair': 'btccad'},
    {'pair': 'btcjpy'},
]

class CryptoPriceIngester:
    def __init__(self,  crypto_client, dal, query_interval=DEFAULT_QUERY_INTERVAL):
        self.query_interval = query_interval
        self.crypto_client = crypto_client
        self.crypto_dal = dal

    def run(self):
        s.enter(self.query_interval, 1, self.query_latest_crypto_prices)
        while True:
            s.run()
            time.sleep(1)
    
    def query_latest_crypto_prices(self, use_default_symbols=True):
        now = int(time.time())
        s.enter(self.query_interval, 1, self.query_latest_crypto_prices)
        
        # We use the default symbols here so we don't hit the api's rate limit.
        currencies = DEFAULT_SYMBOLS
        if not use_default_symbols:
            currencies = self._get_symbols()
        for currency in currencies:
            symbol = currency['pair']
            resp = self.crypto_client.get_price(symbol)
            price = resp['price']
            self.crypto_dal.insert_price(now, symbol, price)
        return ""
    
    def _get_symbols(self):
        return self.crypto_client.get_pairs()