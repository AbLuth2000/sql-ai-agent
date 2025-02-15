from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from src.tools.sql_generator_agent import generate_sql_query
from src.tools.sql_executor_agent import execute_sql_query
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI LLM with GPT-4o-mini
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),  # Default to gpt-4o-mini if env variable is missing
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
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)


def process_user_request(user_request):
    """Runs the AI agent to process a database-related request."""
    try:
        response = sql_agent.run(user_request)
        return response
    except Exception as e:
        return f"❌ Error processing request: {e}"


if __name__ == "__main__":
    user_request = input("Enter your database request: ")
    result = process_user_request(user_request)
    print(f"\n🎯 Result:\n{result}")
