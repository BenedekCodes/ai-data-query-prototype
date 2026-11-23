import unittest

import pandas as pd

from explorer.charts import make_chart


class ChartTests(unittest.TestCase):
    def test_category_result_uses_bar_chart(self):
        chart = make_chart(pd.DataFrame({"region": ["North"], "revenue": [100]}))
        self.assertIsNotNone(chart)
        self.assertEqual(chart.data[0].type, "bar")

    def test_daily_result_uses_line_chart(self):
        chart = make_chart(pd.DataFrame({"order_date": ["2025-01-01"], "revenue": [100]}))
        self.assertIsNotNone(chart)
        self.assertEqual(chart.data[0].type, "scatter")

    def test_monthly_result_uses_line_chart(self):
        chart = make_chart(pd.DataFrame({"month": ["2024-01-01"], "revenue": [100]}))
        self.assertIsNotNone(chart)
        self.assertEqual(chart.data[0].type, "scatter")

    def test_unplottable_results_return_no_chart(self):
        self.assertIsNone(make_chart(pd.DataFrame({"revenue": [100]})))
        self.assertIsNone(make_chart(pd.DataFrame({"region": [], "revenue": []})))
