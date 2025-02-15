from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from src.tools.sql_generator_agent import generate_sql_query
from src.tools.sql_executor_agent import execute_sql_query
from dotenv import load_dotenv
import os
from typing import Optional

# Load environment variables
load_dotenv()

# Initialize OpenAI LLM with GPT-4o-mini
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),  
    temperature=0.2,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Define tools for LangChain agent
generate_sql_tool = Tool(
    name="GenerateSQLQuery",
    func=generate_sql_query,
    description="Converts a natural language request into a valid SQL query."
)

execute_sql_tool = Tool(
    name="ExecuteSQLQuery",
    func=execute_sql_query,
    description="Executes an SQL query and returns the result."
)

# Initialize LangChain agent with tools
tools = [generate_sql_tool, execute_sql_tool]

sql_agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)


def process_user_request(user_request: str) -> Optional[str]:
    """Processes a natural language user request by generating an SQL query and executing it.

    Args:
        user_request (str): The user's database-related request in natural language.

    Returns:
        Optional[str]: The query execution result or an error message if an issue occurs.
    """
    try:
        response: str = sql_agent.run(user_request)

        # If the response is an execution error, stop retrying
        if "SQL Execution Error" in response or "Error" in response:
            return response

        return response

    except Exception as e:
        return f"Error processing request: {e}"

