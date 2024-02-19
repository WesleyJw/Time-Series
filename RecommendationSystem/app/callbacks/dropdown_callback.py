from dash import Input, Output,callback

@callback(
    Output("render-div-id", "children"),
    Input("dropdown-search-id", "value")
)
def search_video(value):
    print('test')
    return 'test'