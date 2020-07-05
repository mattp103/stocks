import sqlite3
from operator import truediv
from statistics import mean
from datetime import datetime, timedelta
from stock_api import company_ids, get_company_current_data


# establish database connection and cursor object
conn = sqlite3.connect("stocks.db")
c = conn.cursor()


class Trader:
    """Class to manage database values individually and test different investment approaches"""
    def __init__(self, name, starting_worth=10000, current_worth=10000):
        with conn:
            c.execute("SELECT * FROM traders WHERE name = :name", {"name": name})

            try: self.pk, self.name, self.starting_worth, self.current_worth, self.current_balance = c.fetchone()  # tries to create variables from object in database
            except TypeError:  # if the object does not exist, therefore this must be a new trader object, so create the new object in the database
                c.execute("INSERT INTO traders VALUES (:id, :name, :starting_worth, :current_worth, :current_balance)",  # create the new object
                          {"id": None, "name": name, "starting_worth": starting_worth, "current_worth": current_worth, "current_balance": starting_worth})

                c.execute("SELECT * FROM traders WHERE name = :name", {"name": name})  # get the new objects values and create the self. variables
                self.pk, self.name, self.starting_worth, self.current_worth, self.current_balance = c.fetchone()

    def buy(self, money, company):
        """local function to buy shares for the trader from company: company; worth £: money"""
        if money <= self.current_balance:  # checks amount to spend is less than the traders balance
            try:
                price = float(get_company_current_data(company)["price"])/100  # price of each stock in £
                quantity = int(money/price)  # how many stocks to be bought
                worth = price*quantity  # worth of these stocks
                date_purchased = str(datetime.now())  # current date and time to store in database

                self.current_balance -= worth  # updates the traders current balance now stocks have been bought

                with conn:  # create investment object in database and update traders balance
                    c.execute("INSERT INTO investments VALUES (?, ?, ?, ?, ?, ?, ?)",
                              (None, quantity, worth, date_purchased, worth, self.pk, company_ids[company]))
                    c.execute("UPDATE traders SET current_balance = current_balance-? WHERE id=?", (worth, self.pk))

            except ValueError:  # occurs if api stock price returns "#N/A"
                print("Stocks cannot be bought for that company right now")

    def sell(self, company, all_shares=True):
        """local function to sell shares for the trader for company: company. If all_shares == True then it will sell all of the current stocks"""
        # TODO have the ability to sell part of the stocks, not all of them
        with conn:
            company_data = self.investments[company]  # gets the investment data from self.investments (dictionary)
            if all_shares:
                self.current_balance += company_data[-1]  # update current balance
                c.execute("DELETE FROM investments WHERE id = ?", (company_data[0],))  # delete investment object in database
                c.execute("UPDATE traders SET current_balance = current_balance + ?", (company_data[-1],))  # update traders current balance in database

    @property
    def investments(self):
        """returns a dictionary of all the traders investments"""
        c.execute("""
        SELECT code, investments.id, quantity, starting_worth, date_purchased, current_worth
        FROM investments INNER JOIN companies ON companies.id = investments.company_id
        WHERE investments.trader_id = ?""", (self.pk,))

        return {investment[0]: investment[1:] for investment in c.fetchall()}  # format = {company_code: (data, ..., ...)}


def average_price_changes(weeks=0.0, days=0.0, hours=0.0):
    # return the average stock price change for all the companies over a specified period
    average_changes = {}  # sorted dict of all the average stock price changes, high to low
    td = timedelta(weeks=weeks, days=days, hours=hours) if weeks or days or hours else timedelta(weeks=1)  # uses function parameters if specified else defaults to 1 week
    now = datetime.now()

    with conn:
        for code, c_id in company_ids.items():  # code = company_identifier and c_id = primary key associated with database
            c.execute("SELECT price, change FROM stocks WHERE company_id = :id AND date_time >= :dt", {"id": c_id, "dt": now-td})  # get price and change since timedelta

            prices, changes = map(list, map(set, zip(*c.fetchall()[::-1])))  # gets all unique prices and changes, so as not to give bias to stock markets closed statistics
            average_changes[code] = (mean(list(map(truediv, map(lambda x: 0 if x == "#N/A" else x, changes), map(lambda x: 1 if x == "#N/A" else x, prices))))*100)  # add average change to dictionary with the key being the companies name

    return {k: v for k, v in sorted(average_changes.items(), key=lambda item: item[1], reverse=True)}  # return the sorted dictionary of price changes


# algorithms
def a1(average_changes, amount_to_spend):
    # first algorithm to simply buy top 5 performing companies
    # TODO check prices every sop often and sell if -5% or +10%
    trader = Trader("A1")  # create trader object with name 'A1'
    if amount_to_spend <= trader.current_balance:  # check trader has enough money
        for amount, code in zip([0.4, 0.25, 0.15, 0.1, 0.1], average_changes.keys()):  # buy percentage based amounts of amount to spend: e.g. Best company = 40% of amount to spend
            trader.buy(amount_to_spend*amount, code)

    print(trader.investments)
    # for data in trader.investments.keys():
    #     trader.sell(data)
    #
    # print(trader.investments)
    #


if __name__ == "__main__":
    a1(average_price_changes(weeks=1), 1000)  # run first algorithm using data from past week
