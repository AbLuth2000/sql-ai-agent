# SQL AI Agent

## Overview

This repository contains an **AI-powered SQL agent** that can generate and execute SQL queries based on natural language requests.

## Features

- Converts natural language requests into **SQL queries**
- Executes the generated queries on an **SQLite database**
- Prevents **unsafe queries** like `DROP` or `DELETE`
- Returns **structured JSON responses**
- Logs executed queries for **debugging**

## How It Works

1. The user enters a request in **plain English**
2. The AI **generates an SQL query**
3. The query is **executed on an SQLite database**
4. The result is **returned as structured JSON**

### Example

#### **User Input:**

```
Show me all users with orders
```

#### **AI Generated SQL:**

```sql
SELECT DISTINCT users.id, users.name, users.email
FROM users
JOIN orders ON users.id = orders.user_id;
```

#### **Result:**

```json
[
  [1, "Alice Johnson", "alice@example.com"],
  [2, "Bob Smith", "bob@example.com"]
]
```

## Installation

### **1. Clone the Repository**

```bash
git clone https://github.com/AbLuth2000/sql-ai-agent.git
cd sql-ai-agent
```

### **2. Install Dependencies (Using Poetry)**

```bash
poetry install
```

### **3. Set Up Environment Variables**

Create a `.env` file and add the following:

```
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL="gpt-4o-mini"
```

## Usage

Run the agent using:

```bash
poetry run python src/main.py
```

## Configuration

- **Modify Database Schema:**  
  To reset or modify the database schema, run:
  ```bash
  poetry run python src/database/initialize_db.py
  poetry run python src/database/insert_db_rows.py
  ```
- **Enable Query Logging:**  
  Queries are logged in `query_logs.txt`. Modify `sql_executor_agent.py` to enable or disable logging.

## License

This project is licensed under the **MIT License**.

## Contact

For questions or contributions, reach out via:  
🔗 **LinkedIn:** [Abhyuday Luthra](https://www.linkedin.com/in/abhyuday-luthra/)  
🐙 **GitHub:** [AbLuth2000](https://github.com/AbLuth2000)
