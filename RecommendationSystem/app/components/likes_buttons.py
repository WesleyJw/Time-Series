from dash import html
import dash_bootstrap_components as dbc

def like_button():
    
    like_btn = dbc.Button(
        ["Like"],
        n_clicks=0,
        className="like-btn",
        id="btn-like-id"
    )
    
    deslike_btn = dbc.Button(
        ["Deslike"],
        n_clicks=0,
        className="deslike-btn",
        id="btn-deslike-id"
    )
    
    return html.Div(
                [
                    like_btn,
                    deslike_btn
                ],
                className="card-likes"
            )