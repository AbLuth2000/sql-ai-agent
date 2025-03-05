import json
from src.agents.main_agent import process_user_request


def main():
    """Handles user interaction with the SQL AI Agent."""
    print("\nSQL AI Agent")
    print("Type your database request or 'exit' to quit.\n")

    while True:
        user_request = input("Your request: ")
        if user_request.lower() in ["exit", "quit"]:
            print("\nExiting...")
            break

        result = process_user_request(user_request)

        print("\nResult:")
        print(json.dumps(result, indent=2))  # Pretty print the response
        print("-" * 50)


if __name__ == "__main__":
    main()
