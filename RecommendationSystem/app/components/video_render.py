from dash import html

def render():
    
    return html.Div(
                [
                    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
                ],
                id="render-div-id",
                className="render_div"
            )