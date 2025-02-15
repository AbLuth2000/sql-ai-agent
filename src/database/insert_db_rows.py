import sqlite3
import random
from faker import Faker
from src.database.config import DB_PATH

# Initialize Faker instance
fake = Faker()

def insert_user():
    """Insert a randomly generated user into the database."""
    name = fake.name()
    email = fake.unique.email()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        user_id = cursor.lastrowid  # Get the new user's ID
        print(f"Added User: {name} ({email}) | ID: {user_id}")
    except sqlite3.IntegrityError:
        print(f"Error: Email {email} already exists.")

    conn.close()
    return user_id  # Return the user ID to use in orders


def insert_order(user_id):
    """Insert a random order linked to a user."""
    total_price = round(random.uniform(20, 500), 2)  # Random price between 20 and 500

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO orders (user_id, total_price) VALUES (?, ?)", (user_id, total_price))
        conn.commit()
        order_id = cursor.lastrowid
        print(f"Added Order: ID {order_id} | User ID {user_id} | Total: ${total_price}")
    except sqlite3.IntegrityError:
        print(f"Error: User ID {user_id} does not exist.")

    conn.close()
    return order_id  # Return order ID for order items


def insert_order_item(order_id):
    """Insert random order items linked to an order."""
    product_name = fake.word().capitalize()  # Random product name
    quantity = random.randint(1, 5)  # Random quantity between 1 and 5
    unit_price = round(random.uniform(5, 200), 2)  # Random price between 5 and 200

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO order_items (order_id, product_name, quantity, unit_price)
            VALUES (?, ?, ?, ?)
        """, (order_id, product_name, quantity, unit_price))
        
        conn.commit()
        print(f"Added Order Item: {product_name} (x{quantity}) | Order ID {order_id} | Price: ${unit_price}")
    except sqlite3.IntegrityError:
        print(f"Error: Order ID {order_id} does not exist.")

    conn.close()


def generate_random_data(num_users=5, max_orders_per_user=3, max_items_per_order=4):
    """Generate random users, orders, and order items."""
    print("\n🚀 Generating Random Data...\n")

    for _ in range(num_users):
        user_id = insert_user()  # Create a user

        num_orders = random.randint(1, max_orders_per_user)  # Random orders per user
        for _ in range(num_orders):
            order_id = insert_order(user_id)  # Create an order

            num_items = random.randint(1, max_items_per_order)  # Random items per order
            for _ in range(num_items):
                insert_order_item(order_id)  # Add order items

    print("\nRandom Data Generation Complete!\n")


# Run the script if executed directly
if __name__ == "__main__":
    generate_random_data(num_users=5, max_orders_per_user=3, max_items_per_order=4)
