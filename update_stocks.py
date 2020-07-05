import sqlite3
from stock_api import get_all_current_data, company_ids
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import time


def insert_prices():
    """Creates new object in stock table, based on current data"""
    data = get_all_current_data()  # gets data from api
    date_time = datetime.datetime.now()
    c_ids, c_codes = company_ids.values(), company_ids.codes()

    with conn:
        for id_code, c_id in zip(c_codes, c_ids):  # create stock for each company
            params = {'id': None, 'price': data[id_code]['price'], 'change': data[id_code]['change'], 'date_time': date_time, 'company_id': c_id}

            c.execute("""
            INSERT INTO stocks
            VALUES (:id, :price, :change, :date_time, :company_id)
            """, params)

    print("Inserted new stock prices at " + date_time.strftime("%H:%M:%S"))


def update_investments():
    """updates investments current_worth every 5 minutes"""
    # TODO make this obsolete using quicker calculation methods not requiring database
    data = get_all_current_data()
    companies = company_ids.items()
    date_time = datetime.datetime.now()

    with conn:
        c.execute("SELECT id FROM traders")
        trader_ids = c.fetchall()  # gets all the traders' ids

        # update investments current worth for each company for each trader
        for pk in trader_ids:
            for code, company in companies:
                try:
                    price = float(data[code]["price"])
                    c.execute("UPDATE investments SET current_worth = quantity*? WHERE trader_id = ? AND company_id = ?", (price, pk[0], company))
                except ValueError:
                    pass

    print("Updated investment's current worth at " + date_time.strftime("%H:%M:%S"))


if __name__ == "__main__":
    conn = sqlite3.connect("stocks.db", check_same_thread=False)
    c = conn.cursor()

    scheduler = BlockingScheduler()
    scheduler.add_job(insert_prices, 'interval', minutes=30)  # inserts prices every 30 mins
    scheduler.add_job(update_investments, "interval", minutes=5)  # updates investments worth every 5 mins
    scheduler.start()

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
