import sqlite3
from src.database.config import DB_PATH
from typing import Union, List, Tuple


def execute_sql_query(sql_query: str) -> Union[str, List[Tuple]]:
    """Executes an SQL query on the SQLite database and returns the results.
    
    Args:
        sql_query (str): The SQL query to execute.
    
    Returns:
        Union[str, List[Tuple]]: 
            - If it's a SELECT query, returns a list of tuples with the results.
            - If it's an INSERT/UPDATE/DELETE query, returns a success message.
            - If there's an error, returns an error message as a string.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)
        if sql_query.strip().lower().startswith("select"):
            results: List[Tuple] = cursor.fetchall()  # Ensure correct typing
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
