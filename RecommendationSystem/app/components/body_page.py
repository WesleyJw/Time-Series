from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

from components.render_group import render_block
from components.card_group import card_block


def body():
    
    return html.Div(
                [
                    render_block(),
                    card_block(),
                    dcc.Store(id='intermediate-value')
                ],
                className="body_div"
            )