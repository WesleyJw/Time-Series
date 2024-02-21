from dash import Input, Output
from dash.exceptions import PreventUpdate
import dash_player as dp

import pandas as pd
import joblib as jb

from scipy.sparse import hstack, csr_matrix

from src import video_forecast

def search_video(app):
    @app.callback(
        Output("render-div-id", "children"),
        Input("dropdown-search-id", "value")
    )
    def update_video(value):
        
        data = video_forecast.compute_prediction(value.lower().replace(" ", "+")).sort_values(by=["forecast"], ascending=False).reset_index(drop=True)
        video_id = data["video_id"][0]
        # statistics.viewCount
        # statistics.likeCount
        # statistics.commentCount
        
        video_player = dp.DashPlayer(
                                id="player",
                                url=f"https://youtu.be/{video_id}",
                                controls=True,
                                width="100%",
                                height="100%",
                            ),
        print(data.head())
        return video_player