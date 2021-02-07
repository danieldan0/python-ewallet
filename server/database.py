import sqlite3

def create_users_db(dir):
    conn = sqlite3.connect(dir)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            balance integer NOT NULL,
                                            balance_limit integer,
                                            UNIQUE(name)
                                        );
    ''')
    return conn

def add_user(conn, name):
    c = conn.cursor()
    sql = ''' INSERT OR IGNORE INTO users(name,balance)
              VALUES(?,?) '''
    c.execute(sql, (name, 0))
    conn.commit()
    return c.lastrowid

def get_user(conn, name):
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name=?", (name,))
    return c.fetchone()[1]

def get_balance(conn, name):
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name=?", (name,))
    return c.fetchone()[2]

def get_balance_limit(conn, name):
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name=?", (name,))
    return c.fetchone()[3]

def set_balance_limit(conn, name, amount):
    c = conn.cursor()
    c.execute("UPDATE users SET balance_limit=? WHERE name=?", (amount, name))

def set_balance(conn, name, amount):
    c = conn.cursor()
    c.execute("UPDATE users SET balance=? WHERE name=?", (amount, name))