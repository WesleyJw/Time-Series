import pandas as pd
import numpy as np
import joblib as jb

from scipy.sparse import hstack, csr_matrix

from src import get_videos_interactions, video_processing_data
#import get_videos_interactions, video_processing_data

def compute_prediction(query):
    
    # 0.7RF + 0.3LGBM
    mdl_rf = jb.load("app/src/models/random_forest_20240217.pkl.z")
    mdl_lgbm = jb.load("app/src/models/lgbm_20240217.pkl.z")
    title_vec = jb.load("app/src/models/title_vectorizer_20240217.pkl.z")

    data = get_videos_interactions.video_table([query])
            
    features = video_processing_data.processing_data(data)
    
    if features.empty:
        return 0
    
    title = features["title"]
    vectorized_title = title_vec.transform(title)
    
    feature_array  = hstack([features.drop(columns="title"), vectorized_title])
    #num_features = csr_matrix(np.array([features["views"], features["views_by_day"]]))
    #feature_array = hstack([num_features, vectorized_title])
    
    #p_rf = mdl_rf.predict_proba(feature_array)[0][1]
    p_lgbm = mdl_lgbm.predict_proba(feature_array)[:, 1]
    
    #p = 0.7 * p_rf + 0.3 * p_lgbm
    p = p_lgbm
    
    data["forecast"] = p
    
    return data

if __name__=="__main__":
    value = "data+science".lower().replace(" ", "+")
    compute_prediction(query=value)