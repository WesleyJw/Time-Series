import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()  # take environment variables from .env.



def data_search(queries):
    print("load")
    youtube=build(
                    'youtube',
                    'v3',
                    developerKey=os.environ['YOUTUBE_KEY'])

    #Make a request to youtube api
    request = youtube.channels().list(
        part='contentDetails',
        forUsername='DisneyMusicVEVO' 
    #you can change the channel name here
    )
    #get a response for api
    response=request.execute()
    print(response)


if __name__ == "__main__":
    queries = ["learning", "data+science", "kaggle"]
    data_search(queries)

"""
curl \
  'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&q=surfing&key=AIzaSyBldujKFmC49HztqtlkTJvbvfuo61LPxjU' \
  --header 'Authorization: Bearer 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' \
  --header 'Accept: application/json' \
  --compressed"""