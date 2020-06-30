import sqlite3
from stock_api import get_all_current_data, company_codes
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import time


def insert_prices():
    data = get_all_current_data()
    date_time = datetime.datetime.now()

    with conn:
        for id_code, i in zip(company_codes.keys(), range(len(company_codes.keys()))):
            params = {'id': None, 'price': data[id_code]['price'],
                      'change': data[id_code]['change'], 'date_time': date_time, 'company_id': i+1}

            c.execute("""
            INSERT INTO stocks
            VALUES (:id, :price, :change, :date_time, :company_id)
            """, params)

    print("Inserted new stock prices at " + date_time.strftime("%H:%M:%S"))


if __name__ == "__main__":
    conn = sqlite3.connect("stocks.db", check_same_thread=False)
    c = conn.cursor()

    scheduler = BlockingScheduler()
    scheduler.add_job(insert_prices, 'interval', minutes=30)
    scheduler.start()

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
