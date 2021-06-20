# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from .data import create_dataframe
from .layout import html_layout


def init_dashboard(server, db):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashapp/",
        external_stylesheets=[
            "/static/dist/css/styles.css",
            "https://fonts.googleapis.com/css?family=Lato",
        ],
    )

    # Load DataFrame
    df = create_dataframe(db)
    # print("COLS", df.columns)
    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = html.Div(
        children=[
            dcc.Graph(
                id="histogram-graph",
                figure={
                    "data": [
                        {
                            "x": df["date"],
                            "text": df["timestamp"],
                            "customdata": df["data"],
                            "name": "Pomodoros by Day",
                            "type": "histogram",
                        }
                    ],
                    "layout": {
                        "title": "Pomodoros by Day",
                        "height": 500,
                        "padding": 150,
                    },
                },
            ),
            create_data_table(df, "database-table"),
            dcc.Graph(
                id="time-histogram-graph",
                figure={
                    "data": [
                        {
                            "x": df["time"],
                            "text": df["timestamp"],
                            "customdata": df["data"],
                            "name": "Pomodoros by Minute.",
                            "type": "histogram",
                        }
                    ],
                    "layout": {
                        "title": "Pomodoros by Minute",
                        "height": 500,
                        "padding": 150,
                    },
                },
            ),
            create_data_table(df, "time-database-table"),
        ],
        id="dash-container",
    )
    return dash_app.server


def create_data_table(df, id_):
    """Create Dash datatable from Pandas DataFrame."""
    table = dash_table.DataTable(
        id=id_,
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        sort_action="native",
        sort_mode="native",
        page_size=300,
    )
    return table