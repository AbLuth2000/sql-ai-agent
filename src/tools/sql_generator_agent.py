from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

# Initialize OpenAI LLM with GPT-4o-mini
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    temperature=0.0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)


def generate_sql_query(user_input: str) -> Optional[str]:
    """Generates an SQL query from a natural language input using GPT-4o-mini.

    Args:
        user_input (str): A natural language request for querying the database.

    Returns:
        Optional[str]: The generated SQL query as a string if successful, None if an error occurs.
    """
    prompt = f"""
    You are an AI assistant that translates human requests into SQL queries for a SQLite database.
    The database contains the following tables:
    
    - users(id, name, email, created_at)
    - orders(id, user_id, order_date, total_price)
    - order_items(id, order_id, product_name, quantity, unit_price)
    
    Convert the following user request into a SQL query:
    "{user_input}"
    
    Only return the SQL query, without explanation.
    """
    
    try:
        response: str = llm.predict(prompt).strip()
        return response
    except Exception as e:
        print(f"Error generating SQL query: {e}")
        return None


if __name__ == "__main__":
    user_request = input("Enter your database request: ")
    sql_query = generate_sql_query(user_request)
    
    if sql_query:
        print(f"Generated SQL Query:\n{sql_query}")
    else:
        print("Failed to generate SQL query.")
