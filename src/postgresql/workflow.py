from langgraph.graph import StateGraph, END
from typing import Dict, Any
from agents.orchestrator import OrchestratorAgent
from agents.analyst import AnalystAgent
from agents.postgresql_writer import PostgreSQLWriterAgent
from agents.postgresql_checker import PostgreSQLCheckerAgent
from agents.executor import ExecutorAgent

# Initialize all agents
orchestrator = OrchestratorAgent()
analyst = AnalystAgent()
postgresql_writer = PostgreSQLWriterAgent()
postgresql_checker = PostgreSQLCheckerAgent()
executor = ExecutorAgent()


# Define State (Shared Information Passed Between Agents)
class AgentState:
    user_input: str
    next_agent: str
    response: Dict[str, Any]


# Initialize LangGraph Workflow
workflow = StateGraph(AgentState)

# Add Nodes (Agents)
workflow.add_node("orchestrator", orchestrator.route_request)
workflow.add_node("analyst", analyst.analyze_request)
workflow.add_node("postgresql_writer", postgresql_writer.generate_query)
workflow.add_node("postgresql_checker", postgresql_checker.validate_query)
workflow.add_node("executor", executor.run_query)

# Define Routing Logic (Edges)
workflow.add_edge("orchestrator", "analyst", condition=lambda state: state.next_agent == "analyst")
workflow.add_edge("orchestrator", "postgresql_writer", condition=lambda state: state.next_agent == "postgresql_writer")
workflow.add_edge("orchestrator", "postgresql_checker", condition=lambda state: state.next_agent == "postgresql_checker")
workflow.add_edge("orchestrator", "executor", condition=lambda state: state.next_agent == "executor")


# Handle Follow-Up Cases
def handle_follow_up(state: AgentState) -> AgentState:
    """If the orchestrator determines more info is needed, ask the user a follow-up question."""
    print(f"Follow-up needed: {state.response['follow_up_question']}")
    user_reply = input("Your response: ")  # Capture user input dynamically
    state.user_input = user_reply
    return state

workflow.add_edge("orchestrator", handle_follow_up, condition=lambda state: state.next_agent == "follow_up")

# Handle Completion
workflow.add_edge("orchestrator", END, condition=lambda state: state.next_agent == "complete")

# Set Entry Point
workflow.set_entry_point("orchestrator")
