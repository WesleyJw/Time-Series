import pandas as pd
from datetime import datetime

def gold_processing(silver_file_path, gold_path):
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = pd.read_parquet(silver_file_path)
    data = data[["id.videoId", "snippet.channelId", "snippet.publishedAt"]]
    
    data["delivery_time"] = current_time
    
    data.to_parquet(f"{gold_path}/gold_video_attributes_{current_time}.parquet", index=False)
    
if __name__=="__main__":
    silver_file_path = "dataset/silver/silver_video_attributes_2024-02-09 15:29:46.parquet"
    gold_path = "dataset/gold"
    gold_processing(silver_file_path, gold_path)