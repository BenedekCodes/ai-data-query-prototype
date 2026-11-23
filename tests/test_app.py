import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest


class AppTests(unittest.TestCase):
    def test_example_displays_sql_results_and_chart(self):
        app = AppTest.from_file("../app.py").run()
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertIn("SELECT region", app.code[0].value)
        self.assertEqual(len(app.dataframe), 1)
        self.assertEqual(len(app.get("plotly_chart")), 1)

    def test_unknown_question_shows_error(self):
        app = AppTest.from_file("../app.py").run()
        app.text_input[0].set_value("An unsupported question")
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertIn("supported example questions", app.error[0].value)

    def test_selecting_another_example_updates_question(self):
        app = AppTest.from_file("../app.py").run()
        app.selectbox[0].select("How does revenue change by day?").run()
        self.assertEqual(app.text_input[0].value, "How does revenue change by day?")
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertIn("SELECT order_date", app.code[0].value)

    def test_trino_mode_displays_results(self):
        with patch("explorer.trino_client.execute_trino_query") as execute:
            execute.return_value = (["region", "revenue"], [("North", 1450.0)])
            app = AppTest.from_file("../app.py").run()
            app.radio[0].set_value("Trino").run()
            app.button[0].click().run()
            self.assertFalse(app.exception)
            self.assertIn("iceberg.demo.orders", app.code[0].value)
            self.assertEqual(len(app.dataframe), 1)
            self.assertEqual(len(app.get("plotly_chart")), 1)

    def test_trino_connection_error_is_displayed(self):
        from trino.exceptions import TrinoConnectionError

        with patch("explorer.trino_client.execute_trino_query", side_effect=TrinoConnectionError("offline")):
            app = AppTest.from_file("../app.py").run()
            app.radio[0].set_value("Trino").run()
            app.button[0].click().run()
            self.assertFalse(app.exception)
            self.assertIn("Trino query failed", app.error[0].value)

    def test_switching_sources_selects_a_supported_question(self):
        app = AppTest.from_file("../app.py").run()
        app.selectbox[0].select("How does revenue change by day?").run()
        app.radio[0].set_value("Trino").run()
        self.assertIn(app.text_input[0].value, app.selectbox[0].options)
