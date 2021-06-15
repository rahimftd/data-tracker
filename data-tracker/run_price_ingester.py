from price_ingester.price_ingester import CryptoPriceIngester
from clients.crypto_client import CryptoClient
from dal.dal import CryptoDAL

client = CryptoClient()
dal = CryptoDAL()
querier = CryptoPriceIngester(client, dal)
querier.run()