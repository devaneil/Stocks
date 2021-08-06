import yfinance as yf
import psycopg2
import psycopg2.extras
import config
import io
import sys

# For special characters encoding and decoding.
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

# Database connection.
connection = psycopg2.connect(host = config.DB_HOST,
                                database = config.DB_NAME,
                                user = config.DB_USER,
                                password = config.DB_PASS)

cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)

# Selecting the symbol of distinct stocks in mention table.
cursor.execute("""
                SELECT DISTINCT(s.symbol)
                FROM stock s
                JOIN mention m
                ON s.id = m.stock_id
                """)
rows = cursor.fetchall()
""" print(rows) """

symbols = [] # List to store all the distinct symbols.
for row in rows:
    symbols.append(row['symbol']) # Appending the symbol in the symbols list.

# Getting stock data from yfinance.
for symbol in symbols:

    ticker = yf.Ticker(symbol)
    hist = ticker.history(start = '2021-07-30', end = '2021-08-06')
    hist.reset_index(level = 0, inplace = True)

    for i in range(len(hist)):
        cursor.execute("""
                    INSERT INTO stock_price (symbol, dt, open, high, low, close, volume)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (symbol, hist['Date'][i], float(hist['Open'][i]), float(hist['High'][i]),
                            float(hist['Low'][i]), float(hist['Close'][i]), int(hist['Volume'][i])))

        connection.commit()
