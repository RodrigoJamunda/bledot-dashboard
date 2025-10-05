import sqlite3
import os
import hashlib
import hmac
from pathlib import Path

# Paths
DB_DIR = Path(__file__).parent.parent / "database"
DB_PATH = DB_DIR / "bledot_users.db"

# Create database if it does not exist
DB_DIR.mkdir(exist_ok=True)

def init_db():
    # Initialize the database with the users table if it does not exist
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        email TEXT,
        role TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # If there are no users, create a default admin user:
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
    # Default admin
        admin_hash = hashlib.sha256("admin".encode()).hexdigest()
        bledot_hash = hashlib.sha256("bledot".encode()).hexdigest()

        cursor.execute(
            "INSERT INTO users (username, password_hash, email, role) VALUES (?, ?, ?, ?)",
            ("admin", admin_hash, None, "admin")
        )
        cursor.execute(
            "INSERT INTO users (username, password_hash, email, role) VALUES (?, ?, ?, ?)",
            ("bledot", bledot_hash, None, "user")
        )
    
    conn.commit()
    conn.close()

def verify_user(username, password):
    """Checks if the username and password are correct"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        return False
    
    stored_hash = result[0]
    input_hash = hashlib.sha256(password.encode()).hexdigest()

    return hmac.compare_digest(stored_hash, input_hash)

def get_user_role(username):
    """Gets the user's role"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        return None
    
    return result[0]

def add_user(username, password, email=None, role="user"):
    """Adds a new user to the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, email, role) VALUES (?, ?, ?, ?)",
            (username, password_hash, email, role)
        )
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
    # User already exists
        success = False
    
    conn.close()
    return success

def change_password(username, new_password):
    """Changes the password of an existing user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    password_hash = hashlib.sha256(new_password.encode()).hexdigest()
    
    cursor.execute(
        "UPDATE users SET password_hash = ? WHERE username = ?",
        (password_hash, username)
    )
    
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    return rows_affected > 0

def list_users():
    """Lists all registered users"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, email, role, created_at FROM users")
    users = cursor.fetchall()
    
    conn.close()
    
    # Convert to list of dictionaries
    users_list = []
    for user in users:
        users_list.append({
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "role": user[3],
            "created_at": user[4]
        })
    
    return users_list

def delete_user(username):
    """Deletes a user by username"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    return rows_affected > 0

    # Initialize the database when importing the module
init_db()  


