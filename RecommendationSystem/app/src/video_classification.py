import pandas as pd
import numpy as np
from datetime import datetime, timezone

from dotenv import load_dotenv
load_dotenv()

from get_videos import video_search, clean_data

def processing_data(df):
    
    df['publishedAt'] = pd.to_datetime(df['publishedAt'], infer_datetime_format=True)
    df["date"] = pd.to_datetime(df['publishedAt'].dt.date)
    
    # Clean data
    df_clean = pd.DataFrame(index=df.index)
    df_clean['title'] = df['title']
    df_clean['publishedAt'] = df['publishedAt']
    df_clean["date"] = df["date"] 
    df_clean["statistics.viewCount"] = df["statistics.viewCount"]
    
    features = pd.DataFrame(index=df_clean.index)
    current_time = datetime.now(timezone.utc)
    features["time_since_pub"] = (pd.to_datetime(current_time) - df_clean["publishedAt"]) / np.timedelta64(1, "D")
    features["views"] = df_clean["statistics.viewCount"]
    features["views_by_day"] = features["views"] / features["time_since_pub"]
    features = features.drop(["time_since_pub"], axis=1)
    
    return features

if __name__=="__main__":
    query = ["data+science"]
    response = video_search(query)
    data = clean_data(response)
    print(processing_data(data))
    