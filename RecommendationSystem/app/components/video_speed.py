from dash import html

def speed():
    
    return html.Div(
                [
                    html.H2(children='Do you like this video?', style={'textAlign':'center', 'margin-top': '10px'}),
                ],
                className="speed-video"
            )