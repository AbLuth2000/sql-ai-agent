from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
from typing import List
import sqlite3
from src.database.config import DB_PATH

# Load environment variables
load_dotenv()

# Initialize OpenAI LLM with GPT-4o-mini
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    temperature=0.2,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)


def get_db_schema() -> List[str]:
    """Fetches the schema (table structures) of the SQLite database.

    Returns:
        List[str]: A list of SQL statements that define the database schema.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema_statements = []
    
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        column_definitions = ", ".join([f"{col[1]} {col[2]}" for col in columns])
        schema_statements.append(f"CREATE TABLE {table_name} ({column_definitions});")
    
    conn.close()
    return schema_statements


def generate_sql_query(user_input: str) -> str:
    """Generates an SQL query from a natural language input using GPT-4o-mini.

    Args:
        user_input (str): A natural language request for querying the database.

    Returns:
        str: The generated SQL query.
    """
    schema = "\n".join(get_db_schema())

    prompt = f"""
    You are an AI assistant that translates human requests into SQL queries for a SQLite database.
    Here is the database schema:
    
    {schema}
    
    Convert the following user request into a SQL query:
    "{user_input}"
    
    Only return the SQL query, without explanation.
    """

    try:
        response: str = llm.predict(prompt).strip()
        return response
    except Exception as e:
        print(f"Error generating SQL query: {e}")
        return "ERROR: Failed to generate SQL"


if __name__ == "__main__":
    user_request = input("Enter your database request: ")
    sql_query = generate_sql_query(user_request)

    if sql_query:
        print(f"Generated SQL Query:\n{sql_query}")
    else:
        print("Failed to generate SQL query.")
