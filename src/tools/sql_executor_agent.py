import sqlite3
from src.database.config import DB_PATH
from typing import Union, List, Tuple


def execute_sql_query(sql_query: str) -> Union[str, List[Tuple]]:
    """Executes an SQL query on the SQLite database and returns the results.

    Args:
        sql_query (str): The SQL query to execute.

    Returns:
        Union[str, List[Tuple]]: The query results or an error message.
    """
    conn: sqlite3.Connection = sqlite3.connect(DB_PATH)
    cursor: sqlite3.Cursor = conn.cursor()

    try:
        # Ensure only a single statement is executed
        statements = sql_query.strip().split(";")
        if len(statements) > 1 and statements[-1] == "":
            statements.pop()  # Remove empty last element if present

        if len(statements) > 1:
            return "Error: Only one SQL statement can be executed at a time."

        cursor.execute(sql_query)
        
        if sql_query.strip().lower().startswith("select"):
            results: List[Tuple] = cursor.fetchall()
        else:
            conn.commit()
            results = "Query executed successfully."
        
        return results

    except sqlite3.Error as e:
        return f"SQL Execution Error: {e}"

    finally:
        conn.close()
