# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import pandas as pd
from datetime import datetime
import json

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google_auth_oauthlib.flow import InstalledAppFlow

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def youtube_authentication():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "./web_scraping/secrets/client_secret_557895431029-2tolo18o0md2k4j2tatfl20oaiqg6fgp.apps.googleusercontent.com.json"
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



def processing_data(response):
    try:
        data = pd.json_normalize(response.get("items"))[["id.kind", "id.videoId", "id.playlistId", "snippet.publishedAt", "snippet.channelId", "snippet.title", "snippet.channelTitle", "snippet.liveBroadcastContent"]]
    except KeyError:
        data = pd.json_normalize(response.get("items"))[["id.kind", "id.videoId", "snippet.publishedAt", "snippet.channelId", "snippet.title", "snippet.channelTitle", "snippet.liveBroadcastContent"]]
        
    return data

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

    return "ok"

if __name__ == "__main__":
    queries = ["learning", "data+science", "kaggle"]
    get_video(queries)