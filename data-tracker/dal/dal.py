import sqlite3

DEFAULT_DB_FILE = 'crypto_prices.db'

class CryptoDAL:
    def __init__(self):
        self.connection = create_db_connection()
        self._initialize_tables()
    
    def _initialize_tables(self):
        create_table_sql = """CREATE TABLE IF NOT EXISTS crypto_prices (
            id integer PRIMARY KEY AUTOINCREMENT,
            timestamp integer,
            symbol text,
            price integer
        );"""

        symbol_index_sql = """CREATE INDEX IF NOT EXISTS idx_symbol_crypto_prices ON crypto_prices (symbol);"""
        try: 
            print("Initializing tables for db...")
            c = self.connection.cursor()
            c.execute(create_table_sql)
            c.execute(symbol_index_sql)
        except Exception as e:
            print("Error intializing tables: " + e.__str__())
            raise e

    def insert_price(self, timestamp, symbol, price):
        insert_price_sql = "INSERT INTO crypto_prices (timestamp, symbol, price) VALUES(?, ?, ?)"
        c = self.connection.cursor()
        c.execute(insert_price_sql, (timestamp, symbol, price))
        self.connection.commit()
        c.close()
        return c.lastrowid
    
    def get_price(self, symbol, min_timestamp):
        get_price_sql = "SELECT timestamp, symbol, price FROM crypto_prices WHERE timestamp>=? AND symbol=? ORDER BY timestamp ASC"
        c = self.connection.cursor()
        c.execute(get_price_sql, (min_timestamp, symbol))
        return c.fetchall()

def create_db_connection(): 
    conn = None
    try:
        conn = sqlite3.connect(DEFAULT_DB_FILE)
    except Exception as e:
        print(e)
    return conn
