from src.tools.sql_generator_agent import generate_sql_query
from src.tools.sql_executor_agent import execute_sql_query

def process_user_request(user_request):
    """Takes a natural language request, generates an SQL query, and executes it."""
    print("\n🤖 Generating SQL Query...")
    sql_query = generate_sql_query(user_request)
    print(f"Generated SQL:\n{sql_query}")

    print("\n⚡ Executing Query...")
    result = execute_sql_query(sql_query)
    return result

if __name__ == "__main__":
    user_request = input("Enter your database request: ")
    result = process_user_request(user_request)
    print(f"\n🎯 Result:\n{result}")
