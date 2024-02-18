from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

from components.video_render import render
from components.search_video import search
from components import card_stats, card_views

def render_block():
    
    return html.Div(
                [
                    render(),
                    html.Div(
                        [
                            search(),
                            html.Div(
                                [
                                    card_views.card(),
                                    card_stats.card(),
                                    card_stats.card()
                                ],
                                className="stats-blocks"
                            ),
                            html.Div(
                                [
                                    
                                ],
                                className="likes-block"
                            )
                        ],
                        className="stats-group"
                        
                    )
                ],
                className="stats-div"
            )