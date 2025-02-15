from src.agents.main_agent import process_user_request


def main():
    """Handles user interaction with the SQL AI Agent."""
    print("\n🤖 Welcome to the SQL AI Agent!")
    print("Type your database request or 'exit' to quit.\n")

    while True:
        user_request = input("💬 Your request: ")
        if user_request.lower() in ["exit", "quit"]:
            print("\nExiting...")
            break

        result = process_user_request(user_request)
        print(f"\nResult:\n{result}\n{'-' * 50}")


if __name__ == "__main__":
    main()
