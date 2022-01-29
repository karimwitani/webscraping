import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import dash_table
from database_queries import *



# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '5%',
    'margin-right': '5%',
    'margin-top': '5%',
    'top': 0,
    'padding': '20px 10px 10px'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970',
    'font-size': 40
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR])
app.title = "Business Dev Analytics"





content_first_row = html.Div(
    [
    html.H2(
        "Current Week",
        style= TEXT_STYLE),
    dbc.Row(
        [
            dbc.Col([
                html.Div("Result",style = {'font-size': 40}),
                html.H4("Intro")
                ],
                style= TEXT_STYLE),
            dbc.Col([
                html.Div("Result"),
                html.H4("In Dev")
                ],
                style= TEXT_STYLE),
            dbc.Col([
                html.Div("Result"),
                html.H4("Meeting Set")
                ],
                style= TEXT_STYLE),
            dbc.Col([
                html.Div("Result"),
                html.H4("Agreement")
                ],
                style= TEXT_STYLE),
            dbc.Col([
                html.Div(result_closed_lost,style = {'font-size': 40}),
                html.H4("Closed Lost")
                ],
                style= TEXT_STYLE),
            dbc.Col([
                html.Div("Result"),
                html.H4("Closed Won")
                ],
                style= TEXT_STYLE),
            dbc.Col([
                html.Div("Result"),
                html.H4("Network")
                ],
                style= TEXT_STYLE),
        ]
    ),
    ],
    style=CONTENT_STYLE
)

df = analysis_4_1
content_second_row = html.Div(
    children=[
    html.H2("Ticket Not Moving",style=TEXT_STYLE),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )
    ],
    style=CONTENT_STYLE
)


content = html.Div(
    [
        html.H1('Analytics Dashboard Template', style=TEXT_STYLE),
        html.Hr(),
        content_first_row,
        html.Hr(),
        content_second_row
    ],
    style=CONTENT_STYLE
)






app.layout = html.Div(
    children = content
    )




"""

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🥑", className="header-emoji"),
                html.H1(
                    children="Avocado Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the behavior of avocado prices"
                    " and the number of avocados sold in the US"
                    " between 2015 and 2018",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": data["Date"],
                                    "y": data["AveragePrice"],
                                    "type": "lines",
                                    "hovertemplate": "$%{y:.2f}"
                                                     "<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Average Price of Avocados",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {
                                    "tickprefix": "$",
                                    "fixedrange": True,
                                },
                                "colorway": ["#17B897"],
                            },
                        },
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": data["Date"],
                                    "y": data["Total Volume"],
                                    "type": "lines",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Avocados Sold",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {"fixedrange": True},
                                "colorway": ["#E12D39"],
                            },
                        },
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

"""



if __name__ == "__main__":
    app.run_server(debug=True)