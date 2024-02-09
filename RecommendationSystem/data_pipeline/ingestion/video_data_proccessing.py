import pandas as pd
import numpy as np
import re
import time

import requests as rq
from bs4 import BeautifulSoup
import json

def data_search(queries):
    for query in queries:
         for page in range(1,2):
            with open("./dataset/raw_data/{}_{}.html".format(query, page), 'r+') as inp:
                page_html = inp.read()
                
                parsed = BeautifulSoup(page_html, "html.parser")
                
                tags = parsed.find_all('a', attrs={"id": "video-title"})
                print()
                for e in tags:
                    #test = e.find("a", {"class": "yt-simple-endpoint style-scope ytd-video-renderer"}).attrs['href']
                    print(e)
                    
                """ if e.has_attr("yt-simple-endpoint style-scope ytd-video-renderer"): 
                        link = e['href']
                        title = e['title']
                        print(link, title)
                        """
                
                        
if __name__=="__main__":
    queries = ["machine+learning", "data+science", "kaggle"]
    data_search(queries)