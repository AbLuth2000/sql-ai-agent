from src.postgresql.workflow import workflow  # Import the LangGraph workflow
from langgraph.graph import END
import sys


def main():
    print("AI Assistant is now running.")
    print("Type 'exit' to quit.")
    
    while True:
        # Get user input
        user_input = input("User Input: ")
        
        if user_input.lower() == "exit":
            print("Exiting.")
            sys.exit(0)

        # Initialize state
        state = {"user_input": user_input}

        # Run the workflow
        for result in workflow.stream(state):
            if result is END:
                print("Task completed. No further actions required.")
                break

            # Extract agent response
            response = result.get("response", {})
            next_agent = result.get("next_agent")

            # Print agent response
            print(f"{next_agent.capitalize()}: {response}")


if __name__ == "__main__":
    main()
