from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd

from components import body_page as bp

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__)

app.layout = dbc.Container(
                            [
                                html.H1(
                                    children='Video Recommendation APP', 
                                    style={'textAlign':'center'},
                                    className="title"),
                                bp.body()
                            ],
                           id="container",
                           fluid=True
                           )

if __name__ == '__main__':
    app.run(debug=True)
