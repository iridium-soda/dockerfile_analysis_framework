"""
This is for doing crawling
"""
import time
import requests
import logging

import configparser

proxy_url = None


def get_url(url):
    """
    Getting data by URL
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }

    

    try:
        # To inspect flow of this section, see {Pic required}
        while True: # Headloop
            # Fetch a proxy
            purl = fetch_proxy()
            pdict = {"http": "http://" + purl, "https": "https://" + purl}
            request_timeout_count = 5 # Init/Reset counter
            
            while request_timeout_count > 0:
                # Send request
                content = requests.get(url, headers=headers, proxies=pdict) 
                
                # If got 200?
                if  content.status_code == 200:
                    return content.json()
                    
                else:
                    logging.warning(
                    f"Wait for {content.status_code}, retrying: count down {request_timeout_count}"
                )
                    time.sleep(30)
                    request_timeout_count-=1

    except Exception as e:
        logging.exception("Unexcepted 429", e)
        return get_url(url)


def fetch_proxy() -> str:
    """
    Get an avaliable proxy via URL
    Return raw ip:port string
    """
    global proxy_url

    if proxy_url is None:
        # Initializing
        config = configparser.ConfigParser()
        try:
            config.read("proxy.cfg")
        except Exception as e:
            logging.exception(e)
        proxy_url = config.get("Proxy", "URL")
        logging.info(f"Initializing Proxy by URL{proxy_url}")

    # Fetching IP proxy
    try:
        # 发送HTTP请求并获取响应
        response = requests.get(proxy_url)

        # 检查响应状态码
        if response.status_code == 200:
            # 读取响应内容
            data = response.text
            logging.info(f"Get new ip proxy: {data}")
            return data.strip()
        else:
            logging.warning(f"Get new ip proxy failed:{response.status_code}. Retry")
            return fetch_proxy()  # Retry
    except requests.exceptions.RequestException as e:
        logging.exception(e)
