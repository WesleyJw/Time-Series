from dash import Input, Output
from dash.exceptions import PreventUpdate

def search_video(app):
    @app.callback(
        Output("render-div-id", "children"),
        Input("dropdown-search-id", "value")
    )
    def update_video(value):
        print('test')
        return 'test'