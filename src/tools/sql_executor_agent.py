import sqlite3
from src.database.config import DB_PATH

def execute_sql_query(sql_query):
    """Executes an SQL query on the SQLite database and returns the results."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)
        if sql_query.strip().lower().startswith("select"):
            results = cursor.fetchall()
        else:
            conn.commit()
            results = "Query executed successfully."
    except sqlite3.Error as e:
        results = f"Error: {e}"

    conn.close()
    return results

if __name__ == "__main__":
    sql_query = input("Enter the SQL query to execute: ")
    result = execute_sql_query(sql_query)
    print(f"Execution Result:\n{result}")
