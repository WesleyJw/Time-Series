import pandas as pd
from datetime import datetime

def silver_processing(bronze_file_path, silver_path):
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = pd.read_parquet(bronze_file_path)
    data = data.drop_duplicates(["id.videoId"])
    
    data["load_ts"] = current_time
    
    data.to_parquet(f"{silver_path}/silver_video_attributes_{current_time}.parquet", index=False)
    
if __name__=="__main__":
    bronze_file_path = "dataset/bronze/youtube_video_macro_informations_2024-02-09 07:49:49.parquet"
    silver_path = "dataset/silver"
    silver_processing(bronze_file_path, silver_path)