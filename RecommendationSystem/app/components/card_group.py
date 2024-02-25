from dash import html
from components.card_mini_video import mini_video

def card_block():
    
    return html.Div(
                [
                    mini_video(id="second"),
                    mini_video(id="third"),
                    mini_video(id="fourth"),
                    mini_video(id="fifth"),
                    mini_video(id="sixth")
                ],
                className="card-group"
            )