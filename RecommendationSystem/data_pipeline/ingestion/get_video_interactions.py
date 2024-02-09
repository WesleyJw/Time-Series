import os
import pandas as pd
from datetime import datetime
import json
from dotenv import load_dotenv
load_dotenv()

from video_search import youtube_authentication


def main():
    """youtube = youtube_authentication()
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id="Ks-_Mh1QhMc,c0KYU2j0TM4,eIho2S0ZahI"
    )
    response = request.execute()

    print(response)"""
    
    dataset = pd.read_parquet("dataset/bronze/youtube_video_macro_informations_2024-02-09 07:49:49.parquet")
    print(dataset.describe())

if __name__ == "__main__":
    main()

