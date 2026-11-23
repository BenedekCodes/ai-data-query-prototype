"""Run the supported example queries against the local Trino stack."""

from contextlib import closing

from trino.dbapi import connect

from explorer.demo import EXAMPLE_QUERIES, sql_for_question


SAMPLE_QUESTIONS = (
    "What is the total revenue by region?",
    "What is the total revenue by product?",
    "How many orders are there by region?",
)

TRINO_QUERIES = {
    question: EXAMPLE_QUERIES[question].replace("FROM orders", "FROM iceberg.demo.orders")
    for question in SAMPLE_QUESTIONS
}
TRINO_QUERIES.update({
    "How does monthly revenue change?": """
        SELECT CAST(date_trunc('month', o.order_date) AS VARCHAR) AS month,
               ROUND(SUM(i.quantity * i.unit_price * (1 - i.discount_rate)), 2) AS revenue
        FROM iceberg.retail.orders o
        JOIN iceberg.retail.order_items i ON o.order_id = i.order_id
        WHERE o.status = 'completed'
        GROUP BY 1
        ORDER BY 1
    """,
    "What are the top products by revenue?": """
        SELECT p.product_name,
               ROUND(SUM(i.quantity * i.unit_price * (1 - i.discount_rate)), 2) AS revenue
        FROM iceberg.retail.orders o
        JOIN iceberg.retail.order_items i ON o.order_id = i.order_id
        JOIN iceberg.retail.products p ON i.product_id = p.product_id
        WHERE o.status = 'completed'
        GROUP BY p.product_id, p.product_name
        ORDER BY revenue DESC, p.product_name
        LIMIT 10
    """,
    "What is profit by region?": """
        SELECT c.region,
               ROUND(SUM(i.quantity * (i.unit_price * (1 - i.discount_rate) - i.unit_cost)), 2) AS profit
        FROM iceberg.retail.orders o
        JOIN iceberg.retail.order_items i ON o.order_id = i.order_id
        JOIN iceberg.retail.customers c ON o.customer_id = c.customer_id
        WHERE o.status = 'completed'
        GROUP BY c.region
        ORDER BY profit DESC, c.region
    """,
})
TRINO_QUESTIONS = tuple(TRINO_QUERIES)


def sql_for_trino_question(question: str) -> str:
    return sql_for_question(question, TRINO_QUERIES)


def execute_trino_query(sql: str) -> tuple[list[str], list[list]]:
    allowed_queries = (sql_for_trino_question(question) for question in TRINO_QUESTIONS)
    if sql not in allowed_queries:
        raise ValueError("Only predefined Trino example queries can be executed.")

    with closing(connect(host="localhost", port=8080, user="explorer", request_timeout=10)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            return columns, cursor.fetchall()
