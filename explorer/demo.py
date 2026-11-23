"""A small, deliberately constrained natural-language-to-SQL demo."""

from contextlib import closing
import sqlite3


EXAMPLE_QUERIES = {
    "What is the total revenue by region?": """
        SELECT region, ROUND(SUM(amount), 2) AS revenue
        FROM orders
        GROUP BY region
        ORDER BY revenue DESC, region
    """,
    "What is the total revenue by product?": """
        SELECT product, ROUND(SUM(amount), 2) AS revenue
        FROM orders
        GROUP BY product
        ORDER BY revenue DESC, product
    """,
    "How many orders are there by region?": """
        SELECT region, COUNT(*) AS order_count
        FROM orders
        GROUP BY region
        ORDER BY order_count DESC, region
    """,
    "How does revenue change by day?": """
        SELECT order_date, ROUND(SUM(amount), 2) AS revenue
        FROM orders
        GROUP BY order_date
        ORDER BY order_date
    """,
}

SAMPLE_ORDERS = [
    ("2025-01-01", "North", "Laptop", 1200.00),
    ("2025-01-01", "South", "Monitor", 300.00),
    ("2025-01-02", "North", "Monitor", 250.00),
    ("2025-01-02", "West", "Laptop", 1100.00),
    ("2025-01-03", "South", "Laptop", 1000.00),
    ("2025-01-03", "West", "Monitor", 350.00),
]


def sql_for_question(question: str) -> str:
    """Return a predefined query, not an LLM-generated query."""
    normalized = " ".join(question.split()).casefold()
    for example, sql in EXAMPLE_QUERIES.items():
        if normalized == example.casefold():
            return sql.strip()
    raise ValueError("Please enter one of the supported example questions exactly.")


def execute_demo_query(sql: str) -> tuple[list[str], list[tuple]]:
    """Run a predefined query against a fresh in-memory sample database."""
    if sql not in (query.strip() for query in EXAMPLE_QUERIES.values()):
        raise ValueError("Only predefined demo queries can be executed.")
    with closing(sqlite3.connect(":memory:")) as connection:
        connection.execute(
            "CREATE TABLE orders (order_date TEXT, region TEXT, product TEXT, amount REAL)"
        )
        connection.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", SAMPLE_ORDERS)
        cursor = connection.execute(sql)
        columns = [column[0] for column in cursor.description]
        return columns, cursor.fetchall()
