# Stocks
**Tracking the change in value of the most talked about stocks in *wallstreetbets* in a given period.**

## Requirements :
**Docker Desktop**

## Instructions :

**1.** Create a paper trading account on : **https://alpaca.markets/** and get the **key** and **secret key**. Change these values in the config file **config.py**. <br>
**2.** Pull TimescaleDB image on docker : **docker run -d --name timescaledb -p 5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb:latest-pg12** <br>
**3.** Execute an interactive bash : **docker exec -it bash** <br>
**4.** Run a PostgreSQL interactive terminal : **psql -U postgres** <br>
**5.** Create the tables on PostgresSQL interactive terminal using the queries on **tables.sql**. <br>
**6.** Populate the stock table using **stock.py**. <br>
**7.** Populate the reddit table using **reddit.py**. <br>
**8.** Populate the price table using **price.py**. <br>
**9.** Run **queries.py**. <br>

## Tables :

**stock** <br>
This table will store the name of the stock, symbol of the stock and the exchange the stock is traded on. <br>
**reddit** <br>
This table will store the time a post was posted, id of the stock, title of the post and link to the post. <br>
**price** <br>
This table will store the data of the stocks mentioned in the subreddit.

## Output :

![Plot](https://user-images.githubusercontent.com/51035563/128588346-7c13d545-b32f-4fb8-a2ec-3a63d2c62d77.jpg)
