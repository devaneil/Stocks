import psycopg2
import psycopg2.extras
import config
import pandas as pd
import pandas.io.sql as sqlio
import matplotlib.pyplot as plt

# Database connection.
connection = psycopg2.connect(host = config.DB_HOST,
                                database = config.DB_NAME,
                                user = config.DB_USER,
                                password = config.DB_PASS)

cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)

# Queries.

# Number of times a stock was mentioned in wallstreetbets.
cursor.execute("""
                SELECT COUNT(*) AS num_mentions, stock_id, symbol
                FROM mention
                JOIN stock on stock.id = mention.stock_id
                GROUP BY stock_id, symbol
                ORDER BY num_mentions DESC
                """)
mentions = cursor.fetchall()

""" for mention in mentions:
    print(mention)
print(mentions[0]) # Most mentioned stock. """

most_symbol = mentions[0][2] # Symbol of most mentioned stock.

# Analyzing the most mentioned stock.
query = """ SELECT *
            FROM stock_price
            WHERE symbol = '{}'
             """.format(most_symbol) # Query to filter out the details of the most mentioned stock.

df = sqlio.read_sql_query(query, connection) # Convertin the SQL query output into pandas dataframe.
""" print (df) """

# Plot.
plt.style.use('seaborn-darkgrid')
df.plot(y = ['open', 'high', 'low', 'close'],
            x = 'dt')
plt.xlabel('Date', fontsize = 12)
plt.ylabel('Price in USD', fontsize = 12)
plt.title('Stock price of {}'.format(most_symbol), fontsize = 12)
plt.show()
