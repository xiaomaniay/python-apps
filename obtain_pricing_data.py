#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import mysql.connector
import lxml
from lxml import html
import requests
import pandas as pd

# Obtain a database connection to the MySQL instance
db_host = 'localhost'
db_user = 'sec_user'
db_pass = '0521Test'
db_name = 'securities_master'
con = mysql.connector.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name)


def obtain_list_of_db_tickers():
    """Obtains a list of the ticker symbols in the database."""

    try:
        cur = con.cursor()
        cur.execute("SELECT id, ticker FROM symbol")
        data = cur.fetchall()
        return [(d[0], d[1]) for d in data]
    except mysql.connector.Error as error:
        con.rollback()
        print('Failed to select id from symbol {}'.format(error))
    finally:
        # closing database connection.
        if con.is_connected():
            cur.close()
            con.close()
            print("MySQL connection is closed")


def get_daily_historic_data_yahoo(ticker,
                                  start_date=(2000, 1, 1),
                                  end_date=datetime.datetime.now()):
    """Obtains data from Yahoo Finance returns and a list of tuples.

    ticker: Yahoo Finance ticker symbol, e.g. "GOOG" for Google, Inc.
    start_date: Start date in (YYYY, M, D) format
    end_date: End date in (YYYY, M, D) format"""

    # Construct the Yahoo URL with the correct integer query parameters
    # for start and end dates. Note that some parameters are zero-based!

    start_timestamp = int((datetime.datetime(start_date[0], start_date[1], start_date[2]) - datetime.datetime(1970, 1, 1)).total_seconds())
    end_timestamp = int((end_date - datetime.datetime(1970, 1, 1)).total_seconds())

    yahoo_url = "https://finance.yahoo.com/quote/%s/history?period1=%s&" \
                "period2=%s&interval=1d&filter=history&frequency=1d" % (ticker, start_timestamp, end_timestamp)
    print(yahoo_url)
    # Try connecting to Yahoo Finance and obtaining the data
    # On failure, print an error message.
    try:
        page = requests.get(yahoo_url)
        tree = html.fromstring(page.content)
        table = tree.xpath('//table')
        yf_data = pd.read_html(lxml.etree.tostring(table[0], method='html'))[0]
        print(len(yf_data))
        prices = []
        for y in yf_data:
            p = y.getchildren()
            p0 = p[0].getchildren()[0].text
            p1 = p[1].getchildren()[0].text
            prices.append((datetime.datetime.strptime(p[0], '%Y-%m-%d'),
                           p[1], p[2], p[3], p[4], p[5], p[6]))
    except Exception as e:
        print("Could not download Yahoo data: %s" % e)
    return prices


def insert_daily_data_into_db(data_vendor_id, symbol_id, daily_data):
    """Takes a list of tuples of daily data and adds it to the
    MySQL database. Appends the vendor ID and symbol ID to the data.

    daily_data: List of tuples of the OHLC data (with
    adj_close and volume)"""

    # Create the time now
    now = datetime.datetime.utcnow()

    # Amend the data to include the vendor ID and symbol ID
    daily_data = [(data_vendor_id, symbol_id, d[0], now, now, d[1], d[2], d[3], d[4], d[5], d[6]) for d in daily_data]

    # Create the insert strings
    column_str = """data_vendor_id, symbol_id, price_date, created_date, 
        last_updated_date, open_price, high_price, low_price, 
        close_price, volume, adj_close_price"""
    insert_str = ("%s, " * 11)[:-2]
    final_str = "INSERT INTO daily_price (%s) VALUES (%s)" % (column_str, insert_str)

    # Using the MySQL connection, carry out an INSERT INTO for every symbol

    try:
        cur = con.cursor()
        cur.executemany(final_str, daily_data)
        con.commit()
        print("Record inserted successfully into the table")
    except mysql.connector.Error as error:
        con.rollback()
        print('Failed to insert data {}'.format(error))
    finally:
        # closing database connection.
        if con.is_connected():
            cur.close()
            con.close()
            print("MySQL connection is closed")


if __name__ == "__main__":
    # Loop over the tickers and insert the daily historical
    # data into the database
    tickers = obtain_list_of_db_tickers()
    for t in tickers:
        print("Adding data for %s" % t[1])
        yf_data = get_daily_historic_data_yahoo(t[1])
        insert_daily_data_into_db('1', t[0], yf_data)
