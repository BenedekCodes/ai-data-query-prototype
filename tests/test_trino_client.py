import unittest
from unittest.mock import patch

from explorer.trino_client import execute_trino_query, sql_for_trino_question


class TrinoClientTests(unittest.TestCase):
    def test_supported_question_uses_qualified_table(self):
        sql = sql_for_trino_question("  WHAT is the total revenue by region? ")
        self.assertIn("FROM iceberg.demo.orders", sql)

    def test_daily_question_is_not_available_for_trino(self):
        with self.assertRaisesRegex(ValueError, "not supported"):
            sql_for_trino_question("How does revenue change by day?")

    def test_arbitrary_sql_is_rejected_before_connection(self):
        with patch("explorer.trino_client.connect") as connect:
            with self.assertRaisesRegex(ValueError, "predefined"):
                execute_trino_query("DROP TABLE iceberg.demo.orders")
            connect.assert_not_called()

    def test_query_returns_column_names_and_rows(self):
        with patch("explorer.trino_client.connect") as connect:
            cursor = connect.return_value.cursor.return_value
            cursor.description = [("region",), ("revenue",)]
            cursor.fetchall.return_value = [["North", 1450.0]]
            sql = sql_for_trino_question("What is the total revenue by region?")
            self.assertEqual(execute_trino_query(sql), (["region", "revenue"], [["North", 1450.0]]))
            cursor.execute.assert_called_once_with(sql)
            cursor.close.assert_called_once()
            connect.return_value.close.assert_called_once()
