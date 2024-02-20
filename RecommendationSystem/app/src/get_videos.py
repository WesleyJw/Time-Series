# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

import googleapiclient.discovery
import googleapiclient.errors
from google_auth_oauthlib.flow import InstalledAppFlow

def youtube_authentication():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = os.environ["CLIENT_SECRET_FILE"]
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"] 
    # Get credentials and create an API client
    #flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    #    client_secrets_file, scopes)
    #credentials = flow.run_console()
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_file,
        scopes
    )
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    
    return youtube

def video_search(query, youtube):
    
    request = youtube.search().list(
            part="snippet",
            maxResults=50,
            publishedAfter="2024-01-01T00:00:00Z",
            q=query
        )
    
    return request.execute()
    


if __name__ == "__main__":
    youtube = youtube_authentication()
    query = ["data+science"]
    response = video_search(query)