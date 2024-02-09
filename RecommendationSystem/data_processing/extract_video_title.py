import os
import pandas as pd
import numpy as np
import json
from datetime import datetime

def read_json(directory_path, file_path):
    with open(directory_path + file_path) as file:
        response = json.load(file)
    return response

def data_summarization(response):
    try:
        return pd.json_normalize(response.get("items"))[["id.kind", "id.videoId", "id.playlistId", "snippet.publishedAt", "snippet.channelId", "snippet.title", "snippet.channelTitle", "snippet.liveBroadcastContent"]]
    except KeyError:
        data = pd.json_normalize(response.get("items"))[["id.kind", "id.videoId", "snippet.publishedAt", "snippet.channelId", "snippet.title", "snippet.channelTitle", "snippet.liveBroadcastContent"]]
        data["id.playlistId"] = np.nan
        return data

def get_files_list(directory_path):
    
    return os.listdir(directory_path)

def data_processing(directory_path, save_path):
    
    file_paths = get_files_list(directory_path)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    dataset = pd.DataFrame()
    for file_path in file_paths:
        response = read_json(directory_path, file_path)
        data = data_summarization(response)
        
        dataset = pd.concat([dataset, data])
    
    dataset["processing_time"] = current_time
    dataset.to_parquet(f"{save_path}/youtube_video_macro_informations_{current_time}.parquet", index=False)

if __name__=="__main__":
    directory_path = "dataset/landing/search/"
    save_path = "dataset/bronze"
    data_processing(directory_path, save_path)