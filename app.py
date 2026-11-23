"""Streamlit entry point for the local demo."""

import sqlite3

import pandas as pd
import streamlit as st
from trino.exceptions import Error as TrinoError, HttpError

from explorer.charts import make_chart
from explorer.demo import EXAMPLE_QUERIES, execute_demo_query, sql_for_question
from explorer.trino_client import TRINO_QUESTIONS, execute_trino_query, sql_for_trino_question


def select_example(source: str) -> None:
    st.session_state[f"question-{source}"] = st.session_state[f"example-{source}"]


st.set_page_config(page_title="Trino AI Explorer", layout="wide")
st.title("Trino AI Explorer")
source = st.radio("Data source", ["Local demo", "Trino"], horizontal=True)
if source == "Trino":
    st.info(
        "Queries run on the local Trino Iceberg table managed by Polaris. "
        "Questions still use predefined SQL, not an LLM."
    )
    examples = TRINO_QUESTIONS
else:
    st.info("Local demo: questions use predefined SQL and in-memory sample data.")
    examples = tuple(EXAMPLE_QUERIES)

st.write("Choose an example or enter one of the supported questions below.")
example = st.selectbox(
    "Example questions", examples, key=f"example-{source}", on_change=select_example, args=(source,)
)
question_key = f"question-{source}"
if question_key not in st.session_state:
    st.session_state[question_key] = example
question = st.text_input("Your question", key=question_key)

if st.button("Explore", type="primary"):
    try:
        if source == "Trino":
            sql = sql_for_trino_question(question)
            columns, rows = execute_trino_query(sql)
        else:
            sql = sql_for_question(question)
            columns, rows = execute_demo_query(sql)
    except (ValueError, sqlite3.Error) as error:
        st.error(str(error))
    except (TrinoError, HttpError) as error:
        st.error(f"Trino query failed: {error}. Check that the local stack is running.")
    else:
        results = pd.DataFrame(rows, columns=columns)
        st.subheader("SQL")
        st.code(sql, language="sql")
        st.subheader("Results")
        st.dataframe(results, hide_index=True)
        chart = make_chart(results)
        if chart is not None:
            st.subheader("Visualisation")
            st.plotly_chart(chart)
        else:
            st.info("No chart is available for this result.")
