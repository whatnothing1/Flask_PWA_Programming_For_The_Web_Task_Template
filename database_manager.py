import sqlite3

# Path to your SQLite database
DB_PATH = "/Users/vivaa/Flask_PWA_Programming_For_The_Web_Task_Template/database/data_source.db"

def get_connection():
    """Return a SQLite connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def check_user(email, password):
    """Return user dict if email and password match, else None."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE email = ? AND password = ?", (email, password))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def list_users():
    """Return all users as a list of dicts."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM user")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def listExtension():
    """Example function to return user list."""
    return list_users()
