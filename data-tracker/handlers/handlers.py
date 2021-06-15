import time, statistics

SECONDS_PER_DAY = 60 * 60 * 24 # 60s/m * 60m/h * 24h/d

class Handler:
    def __init__(self, crypto_client, dal):
        self.crypto_client = crypto_client
        self.dal = dal
    
    def handle_get_currency_dropdown(self):
        response = {
            'result': []
        }
        symbols = self.crypto_client.get_pairs()
        for symbol in symbols:
            response['result'].append({
                'symbol': symbol['pair']
            })
        return response
    
    def handle_get_price_l24h(self, symbol):
        now_minus_24h = int(time.time()) - SECONDS_PER_DAY
        rows = self.dal.get_price(symbol, now_minus_24h)
        parsed_rows = self._parse_crypto_price_rows(rows)
        return {
            'result': parsed_rows,
        }
    
    def _parse_crypto_price_rows(self, rows):
        result = []
        for row in rows:
            result.append({
                'timestamp': row[0],
                'symbol': row[1],
                'price': row[2],
            })
        return result

    def handle_post_rank(self, symbols):
        result = []
        for symbol in symbols:
            prices = self.handle_get_price_l24h(symbol)
            prices_only = []
            for price in prices['result']:
                prices_only.append(price['price'])
            standard_deviation = statistics.stdev(prices_only)
            result.append({'symbol': symbol, 'stdev': standard_deviation})
        result.sort(key=stdev_compare_func, reverse=True)

        return {
            'result': [{'rank': i + 1, 'symbol': result[i]['symbol'], 'stdev': result[i]['stdev']} for i in range(len(result))]
        }


def stdev_compare_func(currency):
    return currency['stdev']