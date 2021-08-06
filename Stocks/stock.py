import config
import alpaca_trade_api as tradeapi
import psycopg2
import psycopg2.extras

# Connection
connection = psycopg2.connect(host = config.DB_HOST,
                                database = config.DB_NAME,
                                user = config.DB_USER,
                                password = config.DB_PASS)

cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)

# Instantiating alpacaAPI
api = tradeapi.REST(config.API_KEY,
                    config.API_SECRET,
                    base_url = config.API_URL)

assets = api.list_assets()
#print(assets)
# Inserting the name, symbol and exchange in the stock table.
for asset in assets:
    print(f'Inserting stock {asset.name} {asset.symbol}')
    cursor.execute("""
                    INSERT into stock (name, symbol, exchange)
                    VALUES (%s, %s, %s)
                    """, (asset.name, asset.symbol, asset.exchange))
# Commiting the inserts.
connection.commit()