from dash import Input, Output
from dash.exceptions import PreventUpdate

from src import get_videos_interactions, video_processing_data

def search_video(app):
    @app.callback(
        Output("render-div-id", "children"),
        Input("dropdown-search-id", "value")
    )
    def update_video(value):
        
        data = get_videos_interactions.video_table([value.lower().replace(" ", "+")])
        
        data = video_processing_data.processing_data(data)
        print(value.lower().replace(" ", "+"))
        return 'test'