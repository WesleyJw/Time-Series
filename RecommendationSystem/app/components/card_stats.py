from dash import html

def card():
    
    return html.Div(
                [
                    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
                ],
                className="card-stats"
            )