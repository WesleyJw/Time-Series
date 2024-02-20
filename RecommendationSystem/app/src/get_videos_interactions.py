import os
import pandas as pd
from datetime import datetime
import json
from dotenv import load_dotenv
load_dotenv()

#from get_videos import youtube_authentication, video_search
from src.get_videos import youtube_authentication, video_search

def statistic_extract(response, youtube):
    
    id_string = ""
    for i in response.get("items"):
        id_string = id_string+","+i.get("id").get("videoId")
    
    id_string = id_string[1:]    
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=id_string
    )
    response = request.execute()
    
    return response

def snippet_table(response):
    
    df_snippet = pd.DataFrame()
    for item in response.get("items"):
        snippet = item.get("snippet")
        del snippet["localized"], snippet["thumbnails"], snippet["liveBroadcastContent"], snippet["description"]
        df_temp = pd.json_normalize(snippet)
        df_temp["video_id"] = item.get("id")
        df_snippet = pd.concat([df_snippet, df_temp])
        
    return df_snippet
        
def statistics_table(response):
        
    df_statistic = pd.DataFrame()
        
    for item in response.get("items"):
        del item["snippet"]
        df_temp = pd.json_normalize(item)
        df_statistic = pd.concat([df_statistic, df_temp])
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_statistic["processing_time"] = current_time
    
    return df_statistic

def video_table(query):
    
    youtube = youtube_authentication()
    response = video_search(query, youtube)
    response = statistic_extract(response, youtube)
    
    table_snippet = snippet_table(response)
    table_stats = statistics_table(response)
    
    table_stats = table_stats.rename(columns={"id": "video_id"})
    df = table_snippet.merge(table_stats, on="video_id", how='left')
    
    return df

if __name__ == "__main__":
    query = ["data+science"]
    print(video_table(query))

