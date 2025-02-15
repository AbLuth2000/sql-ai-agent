from pathlib import Path

# Get the absolute path to the directory where this file is located
BASE_DIR = Path(__file__).resolve().parent

# Define the SQLite database path
DB_PATH = BASE_DIR / "local_database.db"
