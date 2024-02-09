import os
import pandas as pd
from datetime import datetime
import json
from dotenv import load_dotenv
load_dotenv()

from video_search import youtube_authentication, save_data


def statistic_extract(landing_path):
    youtube = youtube_authentication()
    
    dataset = pd.read_parquet("dataset/gold/gold_video_attributes_2024-02-09 15:30:14.parquet")
    
    start_id = 0
    end_id = 24
    step = 25
    
    while dataset.shape[0] > start_id:
        id_string = ""
        for index, row in dataset.loc[start_id:end_id,].iterrows():
            id_string = id_string+","+row["id.videoId"]
        print(id_string)
        
        
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=id_string
        )
        response = request.execute()
        save_data(response, query="video_id_"+str(end_id), path=landing_path)
        
        start_id += step
        end_id += step

        print(id_string)
    

if __name__ == "__main__":
    landing_path = "dataset/landing/videos"
    statistic_extract(landing_path)

