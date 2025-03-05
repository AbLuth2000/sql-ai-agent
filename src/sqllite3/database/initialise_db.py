import sqlite3
from src.database.config import DB_PATH


def initialize_database() -> None:
    """Creates a complex SQLite database with default values, NOT NULL constraints, and foreign key relationships."""
    conn: sqlite3.Connection = sqlite3.connect(DB_PATH)
    cursor: sqlite3.Cursor = conn.cursor()

    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,  -- Name cannot be NULL
        email TEXT UNIQUE NOT NULL,  -- Email must be unique and cannot be NULL
        created_at TEXT DEFAULT CURRENT_TIMESTAMP  -- Auto timestamp when user is added
    );
    """)

    # Create Orders Table (Foreign Key: user_id → users.id)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,  -- User ID cannot be NULL
        order_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- Default to current time
        total_price REAL NOT NULL CHECK (total_price >= 0),  -- Ensure price is non-negative
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # Create Order Items Table (Foreign Key: order_id → orders.id)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,  -- Order ID cannot be NULL
        product_name TEXT NOT NULL,  -- Product name cannot be NULL
        quantity INTEGER NOT NULL CHECK (quantity > 0),  -- Quantity must be greater than 0
        unit_price REAL NOT NULL CHECK (unit_price >= 0),  -- Price must be non-negative
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,  -- Auto timestamp
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
    );
    """)

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print(f"Database initialized successfully at {DB_PATH} with default values and constraints!")


if __name__ == "__main__":
    initialize_database()
