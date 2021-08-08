from psaw import PushshiftAPI
import datetime as dt
import psycopg2
import psycopg2.extras
import config
import io
import sys
import re

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

# Database connection.
connection = psycopg2.connect(host = config.DB_HOST,
                                database = config.DB_NAME,
                                user = config.DB_USER,
                                password = config.DB_PASS)

cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)

# Selecting table stock.
cursor.execute("""
                SELECT * FROM stock
                """)
rows = cursor.fetchall()
""" print(rows) # This will print all the records in stock table. """

# Creating a dictionary to store unique stock symbols as key and id of that symbol as its value.
stocks = {}
for row in rows:
    stocks['$' + row['symbol']] = row['id']

# PushshiftAPI instatiation.
api = PushshiftAPI()

# Setting the start and end date to get posts.
""" End date """
end = dt.date.today()
end_month = int(end.strftime("%#m")) # Removing leading 0.
end_day = int(end.strftime("%#d")) # Removing leading 0.
""" Start date """
start = end - dt.timedelta(days = 7)
start_month = int(start.strftime("%#m")) # Removing leading 0.
start_day = int(start.strftime("%#d")) # Removing leading 0.

# Converting to Unix timestamp.
start_date = int(dt.datetime(start.year, start_month, start_day).timestamp())
end_date = int(dt.datetime(end.year, end_month, end_day).timestamp())

# Getting the submissions in the subreddit.
submissions = list(api.search_submissions(before = end_date,
                                         after = start_date,
                                         subreddit = 'wallstreetbets',
                                         filter = ['url', 'author', 'title', 'subreddit']))

""" print(submissions) """

for submission in submissions:

    words = submission.title.split()
    """ words = [re.sub('[^a-zA-Z0-9]+', '', r) for r in words] # Removing special characters.
    words = [y.upper() for y in words] """
    #print(type(words))
    #print(words)
    cashtags = list(set(filter(lambda word : word.lower().startswith('$'), words)))
    #print(cashtags)

    if len(cashtags) > 0 :

        """ print(cashtags)
        print(submission.title) """

        for cashtag in cashtags :

            submitted_time = dt.datetime.fromtimestamp(submission.created_utc).isoformat() # Changing the datetime format.

            try :

                cursor.execute("""
                                INSERT INTO mention (dt, stock_id, title, url)
                                VALUES (%s, %s, %s, %s)
                                """, (submitted_time, stocks[cashtag], submission.title, submission.url))

                connection.commit()

            except Exception as e :

                print(e)
                connection.rollback()