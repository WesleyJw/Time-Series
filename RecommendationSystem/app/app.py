from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd

from components import body_page as bp
from callbacks.import_callbacks import get_all_callbacks

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__)

app.layout = dbc.Container(
                            [
                                html.H1(
                                    children='Video Recommendation APP', 
                                    style={'textAlign':'center'},
                                    className="title"),
                                bp.body(),
                                html.H4(
                                    children='Wesley Lima - Data Scientist. 2024', 
                                    style={'textAlign':'center', 'padding': '0px', "margin": "0px", "padding-top": "10px"})
                            ],
                           id="container",
                           fluid=True
                           )

get_all_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
