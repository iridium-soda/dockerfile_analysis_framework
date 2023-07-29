"""
This is for doing crawling
"""
import time
import requests

import logging


def get_url(url):
    """
    Getting data by URL
    """
    
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }   

    try:
        content = requests.get(url, headers=headers)
        while content.status_code == 429:
            logging.warning ("Wait for 429, retrying...")
            time.sleep(60)
            content = requests.get(url, headers=headers)


        if content.status_code == 200:
            #logging.debug(f"Request {url} returns the following elements")
            return content.json()
        else:
            return None
    except Exception as e:
        logging.exception ("Unexcepted 429", e)
        return get_url(url)