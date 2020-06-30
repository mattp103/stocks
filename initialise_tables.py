import sqlite3
from stock_api import company_codes


if __name__ == "__main__":
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
        for code, name in company_codes.items():
            c.execute("""
            INSERT INTO companies VALUES (
              :id, :code, :name
            );
            """, {'id': None, 'code': code, 'name': name})

    conn.close()
