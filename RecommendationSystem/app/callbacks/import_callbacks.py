from callbacks import dropdown_callback

def get_all_callbacks(app):
    dropdown_callback.search_video(app)
    dropdown_callback.like_btn(app)
    dropdown_callback.deslike_btn(app)