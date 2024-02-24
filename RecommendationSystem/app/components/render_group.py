from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

from components.video_render import render
from components.search_video import search
from components import card_stats, likes_buttons, video_speed

def render_block():
    
    return html.Div(
                [
                    render(),
                    html.Div(
                        [
                            search(),
                            html.Div(
                                [
                                    card_stats.card_views(),
                                    card_stats.card_like(),
                                    card_stats.card_comment()
                                ],
                                className="stats-blocks"
                            ),
                            video_speed.speed(),
                            likes_buttons.like_button()
                        ],
                        className="stats-group"
                        
                    )
                ],
                className="stats-div"
            )