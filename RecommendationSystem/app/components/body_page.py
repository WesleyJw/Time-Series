from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

def body():
    
    return html.Div(
                [
                    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
                ],
                className="body_div"
            )