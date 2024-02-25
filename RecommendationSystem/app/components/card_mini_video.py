from dash import html

def mini_video(id=id):
    
    return html.Div(
                [
                    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
                ],
                className="card-mini",
                id="mini-video-"+id
            )