from dash import html
from components.card_mini_video import mini_video

def card_block():
    
    return html.Div(
                [
                    mini_video(),
                    mini_video(),
                    mini_video(),
                    mini_video(),
                    mini_video()
                ],
                className="card-group"
            )