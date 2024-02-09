# -*- coding: utf-8 -*-

import os
from datetime import datetime
import json

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

def video_search(token, query, youtube):
    
    if token:
        request = youtube.search().list(
            part="snippet",
            maxResults=50,
            q=query,
            pageToken=token
        )
        response = request.execute()
        return response
    else:
        request = youtube.search().list(
            part="snippet",
            maxResults=50,
            q=query
        )
        response = request.execute()
        return response


def save_data(data, query, path):

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_path = f"{path}/search_result_{query.replace('+', '_')}_{current_time}.json"
        with open(data_path, 'w') as file:
            json.dump(data, file)
        print(">>>>> Saved File!")

def get_video(queries):
    youtube = youtube_authentication()
    path_landing = "dataset/landing/search"
    
    for query in queries:
        token = None
        response = video_search(token, query, youtube)
        
        save_data(response, query, path_landing)
        
        for i in range(0, 4):
            token = response.get("nextPageToken")
            response = video_search(token, query, youtube)
        

            save_data(response, query, path_landing)


if __name__ == "__main__":
    queries = ["learning", "data+science", "kaggle"]
    get_video(queries)
