from dash import Dash, html, dcc, page_registry, page_container
import plotly.express as px
import pandas as pd
import datetime
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "DCRDEX Trading Volumes"


app.layout = html.Div([
    page_container
])

if __name__ == '__main__':
    app.run(debug=False)