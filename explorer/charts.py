"""Choose a simple chart based on the result columns."""

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure


def make_chart(results: pd.DataFrame) -> Figure | None:
    numeric_columns = results.select_dtypes(include="number").columns
    dimension_columns = results.select_dtypes(exclude="number").columns
    if results.empty or len(numeric_columns) == 0 or len(dimension_columns) == 0:
        return None

    dimension = dimension_columns[0]
    measure = numeric_columns[0]
    if dimension in ("order_date", "month"):
        return px.line(results, x=dimension, y=measure, markers=True)
    return px.bar(results, x=dimension, y=measure)
