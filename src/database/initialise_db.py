import sqlite3

DB_PATH = "local_database.db"  # Define the SQLite database file


def initialize_database():
    """Creates a complex SQLite database with default values, NOT NULL constraints, and foreign key relationships."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

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
    print("Database initialized successfully with default values and constraints!")


# Run the function
if __name__ == "__main__":
    initialize_database()
