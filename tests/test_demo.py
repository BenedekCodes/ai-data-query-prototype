import unittest

from explorer.demo import EXAMPLE_QUERIES, execute_demo_query, sql_for_question


class DemoQueryTests(unittest.TestCase):
    def test_questions_are_case_and_whitespace_insensitive(self):
        question = "  WHAT is the total revenue   by region?  "
        self.assertEqual(sql_for_question(question), next(iter(EXAMPLE_QUERIES.values())).strip())

    def test_unknown_question_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "supported example questions"):
            sql_for_question("Delete all orders")

    def test_arbitrary_sql_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "predefined"):
            execute_demo_query("DROP TABLE orders")

    def test_revenue_by_region(self):
        sql = sql_for_question("What is the total revenue by region?")
        columns, rows = execute_demo_query(sql)
        self.assertEqual(columns, ["region", "revenue"])
        self.assertEqual(rows, [("North", 1450.0), ("West", 1450.0), ("South", 1300.0)])

    def test_all_example_queries_return_results(self):
        for question in EXAMPLE_QUERIES:
            with self.subTest(question=question):
                columns, rows = execute_demo_query(sql_for_question(question))
                self.assertEqual(len(columns), 2)
                self.assertTrue(rows)


if __name__ == "__main__":
    unittest.main()
