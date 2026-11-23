"""Opt-in checks against the running, seeded local lakehouse."""

import os
import unittest

from explorer.trino_client import execute_trino_query, sql_for_trino_question


@unittest.skipUnless(os.environ.get("TRINO_INTEGRATION_TESTS") == "1", "requires local Trino")
class RetailIntegrationTests(unittest.TestCase):
    def test_monthly_revenue(self):
        columns, rows = execute_trino_query(sql_for_trino_question("How does monthly revenue change?"))
        self.assertEqual(columns, ["month", "revenue"])
        self.assertEqual(len(rows), 24)
        self.assertEqual(rows[0][0], "2024-01-01")
        self.assertAlmostEqual(rows[0][1], 26934.2)
        self.assertEqual(rows[-1][0], "2025-12-01")
        self.assertAlmostEqual(rows[-1][1], 19692.6)

    def test_top_products(self):
        columns, rows = execute_trino_query(sql_for_trino_question("What are the top products by revenue?"))
        self.assertEqual(columns, ["product_name", "revenue"])
        self.assertEqual(len(rows), 10)
        self.assertEqual(rows[0][0], "Product 30")
        self.assertAlmostEqual(rows[0][1], 66220.0)
        self.assertTrue(all(rows[index][1] >= rows[index + 1][1] for index in range(len(rows) - 1)))

    def test_profit_by_region(self):
        columns, rows = execute_trino_query(sql_for_trino_question("What is profit by region?"))
        self.assertEqual(columns, ["region", "profit"])
        self.assertEqual({row[0] for row in rows}, {"North", "South", "East", "West"})
        self.assertAlmostEqual(dict(rows)["East"], 76754.6)
