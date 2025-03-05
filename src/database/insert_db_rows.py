import sqlite3
import random
from faker import Faker
from src.database.config import DB_PATH
from typing import Optional

# Initialize Faker instance
fake = Faker()

def insert_user() -> Optional[int]:
    """Insert a randomly generated user into the database.

    Returns:
        Optional[int]: The newly created user ID, or None if an error occurs.
    """
    name: str = fake.name()
    email: str = fake.unique.email()

    conn: sqlite3.Connection = sqlite3.connect(DB_PATH)
    cursor: sqlite3.Cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        user_id: int = cursor.lastrowid  # Get the new user's ID
        print(f"Added User: {name} ({email}) | ID: {user_id}")
        return user_id
    except sqlite3.IntegrityError:
        print(f"Error: Email {email} already exists.")
        return None
    finally:
        conn.close()


def insert_order(user_id: int) -> Optional[int]:
    """Insert a random order linked to a user.

    Args:
        user_id (int): The ID of the user placing the order.

    Returns:
        Optional[int]: The newly created order ID, or None if an error occurs.
    """
    total_price: float = round(random.uniform(20, 500), 2)  # Random price between 20 and 500

    conn: sqlite3.Connection = sqlite3.connect(DB_PATH)
    cursor: sqlite3.Cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO orders (user_id, total_price) VALUES (?, ?)", (user_id, total_price))
        conn.commit()
        order_id: int = cursor.lastrowid
        print(f"Added Order: ID {order_id} | User ID {user_id} | Total: ${total_price}")
        return order_id
    except sqlite3.IntegrityError:
        print(f"Error: User ID {user_id} does not exist.")
        return None
    finally:
        conn.close()


def insert_order_item(order_id: int) -> None:
    """Insert random order items linked to an order.

    Args:
        order_id (int): The ID of the order.
    """
    product_name: str = fake.word().capitalize()  # Random product name
    quantity: int = random.randint(1, 5)  # Random quantity between 1 and 5
    unit_price: float = round(random.uniform(5, 200), 2)  # Random price between 5 and 200

    conn: sqlite3.Connection = sqlite3.connect(DB_PATH)
    cursor: sqlite3.Cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO order_items (order_id, product_name, quantity, unit_price)
            VALUES (?, ?, ?, ?)
        """, (order_id, product_name, quantity, unit_price))
        
        conn.commit()
        print(f"Added Order Item: {product_name} (x{quantity}) | Order ID {order_id} | Price: ${unit_price}")
    except sqlite3.IntegrityError:
        print(f"Error: Order ID {order_id} does not exist.")
    finally:
        conn.close()


def generate_random_data(num_users: int = 5, max_orders_per_user: int = 3, max_items_per_order: int = 4) -> None:
    """Generate random users, orders, and order items.

    Args:
        num_users (int, optional): Number of users to generate. Defaults to 5.
        max_orders_per_user (int, optional): Max orders per user. Defaults to 3.
        max_items_per_order (int, optional): Max items per order. Defaults to 4.
    """
    print("\nGenerating Random Data...")

    for _ in range(num_users):
        user_id: Optional[int] = insert_user()  # Create a user
        if user_id is None:
            continue  # Skip if user wasn't created

        num_orders: int = random.randint(1, max_orders_per_user)  # Random orders per user
        for _ in range(num_orders):
            order_id: Optional[int] = insert_order(user_id)  # Create an order
            if order_id is None:
                continue  # Skip if order wasn't created

            num_items: int = random.randint(1, max_items_per_order)  # Random items per order
            for _ in range(num_items):
                insert_order_item(order_id)  # Add order items

    print("\nRandom Data Generation Complete!\n")


# Run the script if executed directly
if __name__ == "__main__":
    generate_random_data(num_users=5, max_orders_per_user=3, max_items_per_order=4)
