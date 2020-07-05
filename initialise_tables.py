import sqlite3


if __name__ == "__main__":
    # establish connection and create cursor object
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()

    with conn:
        # create companies table
        c.execute("""
        CREATE TABLE IF NOT EXISTS companies (
          id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
          code text,
          name text
        );""")

        # create stocks table
        c.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
          id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
          price real,
          change real,
          date_time text,
          company_id int,
          FOREIGN KEY (company_id) REFERENCES companies(id)
        );""")

        # create companies
        # for code, name in company_codes.items():
        #     c.execute("""
        #     INSERT INTO companies VALUES (
        #       :id, :code, :name
        #     );
        #     """, {'id': None, 'code': code, 'name': name})

        # create traders table
        c.execute("""
        CREATE TABLE IF NOT EXISTS traders (
          id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
          name text,
          starting_worth real,
          current_worth real,
          current_balance real
        );""")

        # create investments table
        c.execute("""
        CREATE TABLE IF NOT EXISTS investments (
        
          id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
          quantity int,
          starting_worth real,
          date_purchased text,
          current_worth real,
          trader_id int,
          company_id int,
          FOREIGN KEY (trader_id) REFERENCES traders(id),
          FOREIGN KEY (company_id) REFERENCES companies(id)
        )""")
