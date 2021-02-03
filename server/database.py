import sqlite3

def create_users_db(dir):
    conn = sqlite3.connect(dir)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            balance integer NOT NULL,
                                            balance_limit integer
                                        );
    ''')
    return conn