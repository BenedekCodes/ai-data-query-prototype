"""Run the supported example queries against the local Trino stack."""

from contextlib import closing

from trino.dbapi import connect

from explorer.demo import EXAMPLE_QUERIES, sql_for_question


TRINO_QUESTIONS = (
    "What is the total revenue by region?",
    "What is the total revenue by product?",
    "How many orders are there by region?",
)


def sql_for_trino_question(question: str) -> str:
    sql = sql_for_question(question)
    if sql not in (EXAMPLE_QUERIES[example].strip() for example in TRINO_QUESTIONS):
        raise ValueError("This question is not supported by the Trino sample table.")
    return sql.replace("FROM orders", "FROM iceberg.demo.orders")


def execute_trino_query(sql: str) -> tuple[list[str], list[list]]:
    allowed_queries = (sql_for_trino_question(question) for question in TRINO_QUESTIONS)
    if sql not in allowed_queries:
        raise ValueError("Only predefined Trino example queries can be executed.")

    with closing(connect(host="localhost", port=8080, user="explorer", request_timeout=10)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            return columns, cursor.fetchall()
