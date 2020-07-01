import sqlite3
from operator import truediv
from statistics import mean
from datetime import datetime, timedelta

from stock_api import company_ids

conn = sqlite3.connect("stocks.db")
c = conn.cursor()


def average_price_changes(weeks=0.0, days=0.0, hours=0.0):
    # return the average stock price change for all the companies
    average_changes = []  # sorted list of all the average stock price changes
    td = timedelta(weeks=weeks, days=days, hours=hours) if weeks or days or hours else timedelta(weeks=1)
    now = datetime.now()

    with conn:
        for code, c_id in company_ids.items():
            c.execute("SELECT price, change FROM stocks WHERE company_id = :id AND date_time >=  :dt", {"id": c_id, "dt": now-td})

            prices, changes = map(list, map(set, zip(*c.fetchall()[::-1])))  # gets all unique prices and changes
            average_changes.append(mean(list(map(truediv, map(lambda x: 0 if x == "#N/A" else x, changes), map(lambda x: 1 if x == "#N/A" else x, prices))))*100)

    return sorted(average_changes, reverse=True)


if __name__ == "__main__":
    print(average_price_changes(weeks=1))
