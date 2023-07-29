"""
To get images' manifest of each tag which crawed in the last step
Input: paths of image list like results/all_images_a.list
"""

import json
import time
import requests
import sys

#registryBase='https://registry-1.docker.io'
#authBase='https://auth.docker.io'
#authService='registry.docker.io'

def get_url(url, headers):
    try:
        if headers == "":
            content = requests.get(url)
        else:
            content = requests.get(url, headers=headers)

        while content.status_code == 429:
            print("Get 429! Retrying...")
            time.sleep(60)

            if headers == "":
                content = requests.get(url)
            else:
                content = requests.get(url, headers=headers)

        if content.status_code == 200:
            return content
        else:
            print ("Get ",content.status_code)
            print(content)
            return ""
    except:
        return ""

# get token to access the registry 
def auth_repo_token(image):
    url= "https://auth.docker.io/token?service=registry.docker.io&scope=repository:{}:pull".format(str(image))
	
    content = get_url(url, "")
    try:
        print(content.json())
        token = content.json()["token"]
        print("Get token:",token)
        return token
    except:
        raise ValueError("Unable to get token")
        return ""

# get images' manifest
def get_image_manifest(image, tags):
    manifest = []

    if "/" not in image:
        image = "library/" + image

    # get token
    token = auth_repo_token(image)
    if token == "":
        print ("[ERR] Token get failed...")
        return manifest
    
    # get the manifest
    headers = {
        'Authorization': f"Bearer {token}",
        'Accept': 'application/vnd.docker.distribution.manifest.v2+json',
    }

    for tag in tags:# FIXME: Got 404 error. see https://stackoverflow.com/questions/57316115/get-manifest-of-a-public-docker-image-hosted-on-docker-hub-using-the-docker-regi
        url = "https://registry-1.docker.io/v2/{}/manifests/{}".format(str(image), str(tag))
        content = get_url(url, headers)
        if content != "":
            manifest.append(content.json())
    
    return manifest

# function1: url in layers
def judge_url_layers(image, tags):
    urls = []
    # get manifest
    manifests = get_image_manifest(image, tags)

    # error situations
    if len(manifests) == 0:
        return urls

    for manifest in manifests:# TODO:这里要改
        if "layers" not in manifest:
            continue

        for item in manifest['layers']:
            if "urls" in item:
                if item["urls"] not in urls:
                    urls.append(item["urls"])
    return urls
def get_tags(image:str)->list[str]:
    """
    Crawling tags for the given image
    https://docs.docker.com/registry/spec/api/#get-tags
    GET /v2/<name>/tags/list
    Host: <registry host>
    Authorization: <scheme> <token>
    """
    if "/" not in image:
        image = "library/" + image
    tags=[]
    
    # get token
    token = auth_repo_token(image)
    if token == "":
        print ("[ERR] Token get failed...")
        # TODO: maybe... retry?
        return tags
    
    # get the manifest
    headers = {
        'Authorization': f"Bearer {token}",
        'Accept': 'application/vnd.docker.distribution.manifest.v2+json',
    }
    url = "https://registry-1.docker.io/v2/{}/tags/list".format(str(image))
    content = get_url(url, headers)

    if content != "" and "tags" in content.json():
        tags=content.json()["tags"]
    else:
        print("{} seems to have no tags. Something went wrong".format(image))
        return []
    
    print("{} has the following tags:{}".format(image,tags))
    return tags
    
    
# test


def do_crawling(image:str):
    """
    To get all jobs done
    Input: image name like nunomso/javahelloworld_autobuild
    """
    tags=get_tags(image)
    print(judge_url_layers(image,tags))


   
if __name__=="__main__":
    if len(sys.argv) != 2:
        print("Usage: python download.py [path to images list]")
        do_crawling("ubuntu")#Only for test Comment it later
        sys.exit(1)
    path=sys.argv[1]
    print("Get Path:",path)
    try:
        with open(path, 'r') as file:
            tmp = file.readlines() # Raw content of images
            # Strip it
            images=[t.split(",")[0] for t in tmp]
        # TODO
    except IOError as e:
        raise IOError("Invaild path")
    # Doing crawling
    for image in images:
        print("Analysising ",image)
        do_crawling(image)
