from dash import html, dcc

def search():
    
    return html.Div(
                [
                    dcc.Dropdown(
                        ["Kagle", "Learning", "Data Science"],
                        "Data Science",
                        id="dropdown-search-id",
                        className="dropdown-search"
                    )
                ],
                className="search-video"
            )