from dash import Input, Output, html
from dash.exceptions import PreventUpdate
import dash_player as dp

from src import video_forecast

def search_video(app):
    @app.callback(
        [
            Output("render-div-id", "children"),
            Output("card-views-id", "children"),
            Output("card-like-id", "children"),
            Output("card-comment-id", "children"),
            Output("mini-video-second", "children"),
            Output("mini-video-third", "children"),
            Output("mini-video-fourth", "children"),
            Output("mini-video-fifth", "children"),
            Output("mini-video-sixth", "children")
         ],
        Input("dropdown-search-id", "value"),
        PreventUpdate=True
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
                            )
        
        views_stats = html.Div([
            html.H3(f"{data['statistics.viewCount'][0]}", className="car-views-title"),
            html.P("Views", style={'textAlign':'center'})
        ])
        
        likes_stats = html.Div([
            html.H3(f"{data['statistics.likeCount'][0]}", className="car-likes-title"),
            html.P("Likes", style={'textAlign':'center'})
        ])
        
        comments_stats = html.Div([
            html.H3(f"{data['statistics.commentCount'][0]}", className="car-likes-title"),
            html.P("Comments", style={'textAlign':'center'})
        ])
        
        second = dp.DashPlayer(
                                id="player",
                                url=f"https://youtu.be/{data['video_id'][1]}",
                                controls=True,
                                width="100%",
                                height="100%",
                            )
        
        third = dp.DashPlayer(
                                id="player",
                                url=f"https://youtu.be/{data['video_id'][2]}",
                                controls=True,
                                width="100%",
                                height="100%",
                            )
        
        fourth = dp.DashPlayer(
                                id="player",
                                url=f"https://youtu.be/{data['video_id'][3]}",
                                controls=True,
                                width="100%",
                                height="100%",
                            )
        
        fifth = dp.DashPlayer(
                                id="player",
                                url=f"https://youtu.be/{data['video_id'][4]}",
                                controls=True,
                                width="100%",
                                height="100%",
                            )
        
        sixth = dp.DashPlayer(
                                id="player",
                                url=f"https://youtu.be/{data['video_id'][5]}",
                                controls=True,
                                width="100%",
                                height="100%",
                            )
        
        print(data.head())
        return video_player, views_stats, likes_stats, comments_stats, second, third, fourth, fifth, sixth