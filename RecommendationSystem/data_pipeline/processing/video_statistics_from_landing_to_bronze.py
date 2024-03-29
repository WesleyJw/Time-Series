import os
import pandas as pd
from datetime import datetime
from extract_video_attributes import read_json

def snippet_summarize(response):
    
    df_snippet = pd.DataFrame()
    for item in response.get("items"):
        snippet = item.get("snippet")
        del snippet["localized"], snippet["thumbnails"], snippet["liveBroadcastContent"], snippet["description"]
        df_temp = pd.json_normalize(snippet)
        df_temp["video_id"] = item.get("id")
        df_snippet = pd.concat([df_snippet, df_temp])
        
    return df_snippet

def snippet_table(landing_path, bronze_path):
    file_paths = os.listdir(landing_path)
    
    df_snippet = pd.DataFrame()
    for file in file_paths:
        response = read_json(directory_path=landing_path, file_path=file)
        df_snippet = pd.concat([df_snippet, snippet_summarize(response)])
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_snippet["processing_time"] = current_time
    
    df_snippet.to_parquet(f"{bronze_path}snippet_table_{current_time}.parquet", index=False)
        
def statistics_table(landing_path, bronze_path):
    file_paths = os.listdir(landing_path)
    
    df = pd.DataFrame()
    for file in file_paths:
        response = read_json(directory_path=landing_path, file_path=file)
        
        df_statistic = pd.DataFrame()
           
        for item in response.get("items"):
            del item["snippet"]
            df_temp = pd.json_normalize(item)
            df_statistic = pd.concat([df_statistic, df_temp])
        
        df = pd.concat([df, df_statistic])
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df["processing_time"] = current_time
    df.to_parquet(f"{bronze_path}statisctcs_table_{current_time}.parquet", index = False)

if __name__=="__main__":
    landing_path = "dataset/landing/videos/"
    bronze_path = "dataset/bronze/"
    statistics_table(landing_path, bronze_path)
    #print(pd.json_normalize(res))
    #print(snippet_table(response))
