import os
import pandas as pd
from datetime import datetime
from extract_video_attributes import read_json

     
def merge_tables(snippet_name, statistics_name, silver_path):
        
    snippet = pd.read_parquet(f"dataset/bronze/{snippet_name}")
    statistics = pd.read_parquet(f"dataset/bronze/{statistics_name}")
    statistics = statistics.rename(columns={"id": "video_id"})
    general_table = snippet.merge(statistics, on="video_id", how="left")
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    general_table["processing_time"] = current_time
    general_table.to_parquet(f"{silver_path}general_table_youtube_{current_time}.parquet", index = False)
    general_table.drop(columns=["tags"]).to_csv(f"{silver_path}general_table_youtube_{current_time}.csv", index = False, encoding="utf-8")

if __name__=="__main__":
    snippet_name = "snippet_table_2024-02-09 18:08:36.parquet"
    statistics_name = "statisctcs_table_2024-02-10 05:43:41.parquet"
    silver_path = "dataset/silver/"
    merge_tables(snippet_name, statistics_name, silver_path)
