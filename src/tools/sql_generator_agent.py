from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI LLM with GPT-4o-mini
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    temperature=0.2,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)


def generate_sql_query(user_input):
    """Generates an SQL query from natural language input."""
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
    
    response = llm.predict(prompt)
    return response.strip()

if __name__ == "__main__":
    user_request = input("Enter your database request: ")
    sql_query = generate_sql_query(user_request)
    print(f"Generated SQL Query:\n{sql_query}")
