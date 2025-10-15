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
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM user")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def listExtension():
    return list_users()

# ----------------------
# POSTS / LIKES / COMMENTS TABLES
# ----------------------
def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Posts
    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Likes
    cur.execute("""
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            FOREIGN KEY(post_id) REFERENCES posts(id)
        )
    """)

    # Comments
    cur.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(post_id) REFERENCES posts(id)
        )
    """)

    conn.commit()
    conn.close()

# Run on import
create_tables()
