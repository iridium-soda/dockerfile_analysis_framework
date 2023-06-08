"""
To get proxy from local pool
"""
import requests
import logging
url="http://v2.api.juliangip.com/dynamic/getips?num=1&pt=1&result_type=text&split=1&trade_no=1284724384653215&sign=c5ebf19a42ee5892e8958bd1021369ea" #NOTE: Change it before running
test_url='https://hub.docker.com/'

def get_proxy():

    response = requests.get(url)
    # Test
    resp=response.text
    try:
        bis=resp.split(":")
        _,_=bis[0],bis[1]
        print("Extract ",resp)
        proxy={
            "http": "http://"+resp,
            "https": "http://"+resp
        }
        return proxy
    except Exception as e:
        print("Get unexcept message {}",resp)
        return {}
def test_proxy(proxy:dict):
    """
    To test if the proxy is reachable
    """
    try:
        response = requests.get(test_url,proxies=proxy)
        response.raise_for_status()  # 检查是否有HTTP错误
    except requests.exceptions.RequestException as e:
        print("请求错误：", e)
if __name__=="__main__":
    p=get_proxy()
    test_proxy(p)