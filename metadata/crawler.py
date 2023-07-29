"""
Here saves worker functions for crawling metadata of images
"""
import os
import logging
import utils
from dao import *
import concurrent.futures

db=None
def do_crawling(image_list_path:str):
    """
    Main function to crawl metadatas with multi-threads.
    """
    global db
    db=database()
    logging.info("Start crawling")
    try:
        with open(image_list_path, 'r') as fd:
            images = fd.readlines()   
    except FileNotFoundError:
        logging.exception("Images list not found ")
    except PermissionError:
        logging.exception('Permission denied to read ',image_list_path)
    except Exception as e:
        logging.exception('An exception occurs:', e)

    num_images = len(images)
    num_cores =  os.cpu_count() # To fit the current running meachines
    logging.info(f"Ready to run crawling:{num_images} images and the machine has {num_cores} cores")

    # 使用线程池并发处理
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_cores) as executor:
        futures = [executor.submit(worker, raw_image,index,num_images) for index,raw_image in enumerate(images)] 
        # Here raw_image is the original string like 779425102/python27_36_centos7_bad_flask_spider, 2022-04-20T16:30:56.296814Z, 2022-05-04T15:57:33.318458Z

        # 等待所有线程完成
        for future in concurrent.futures.as_completed(futures):
            _,_ = future.result() # 这里index是传进去的index，即当前镜像是文件中第几个
            

def worker(raw_image:str,index:int,num_images:int)->list:
    """
    Main worker functions to get metadata by raw_image string
    input:779425102/python27_36_centos7_bad_flask_spider, 2022-04-20T16:30:56.296814Z, 2022-05-04T15:57:33.318458Z
    """
    result=dict()
    image_name_full,created,updated=raw_image.split(",")
    image_name_full,created,updated=image_name_full.strip(),created.strip(),updated.strip()
    if "/" not in image_name_full and not image_name_full.startswith("/"):#namespace/author
        logging.warning(f"Image:{raw_image} has no namespace,skip.")
        logging.info(f"[{index + 1}/{num_images}] {image_name_full} processed")
        return [0,-1]

    namespace,image=image_name_full.split("/")
    result["namespace"],result["image_name"],result["created"],_=namespace,image,created,updated 
    # getting update date in the overview
    logging.info(f"[{index + 1}/{num_images}] Image {namespace}/{image} record created")

    # Start doing crawling by image name

    # Get overview
    retry,max_retries=0,5
    while retry<max_retries:
        try:
            content=utils.get_url(f"https://hub.docker.com/v2/repositories/{namespace}/{image}/")
            if content==None:
                logging.info(f"[404] {namespace}/{image} has been deleted")
                logging.info(f"[{index + 1}/{num_images}] {image_name_full} processed")
                return [index,raw_image]
            
            result['description']=content['description']
            try:# FIXED: Occasionally, when an image has a very brief description, it may not have a 'full_description' field.
                result['full_description']=content['full_description']
            except:
                result['full_description']=result['description']
            result['updated']=content['last_updated']
            result['pull_count']=content['pull_count']
            break
        except:
            if retry==max_retries:
                logging.exception(f"Image {image_name_full} get wrong resp while getting description; stop retrying {retry}")
                
                break
            logging.warning(f"Image {image_name_full} get wrong resp while getting description; retrying {retry}: URL is https://hub.docker.com/v2/repositories/{namespace}/{image}/")
            logging.debug(content)
            retry+=1

    # get tags 
    result['tags']=get_tags(namespace,image)

    # get update date, layer size, build history, etc. for each digest
    # by https://hub.docker.com/v2/repositories/library/ubuntu/tags/18.04/images
    result['images']={} # group by tag
    for tag in result['tags']:
        result['images'][tag]=get_images_by_tag(namespace,image,tag)

    # write results to database
    db.add(result)

    logging.info(f"[{index + 1}/{num_images}] {image_name_full} processed")
    
    return [index,raw_image]


    

def get_tags(namespace,image)->list[str]:
    """
    To get tags of the given image
    """
    page=1
    tags=list()

    flip_flag=True # to determine if it's still needs to flip pages
    url=f"https://hub.docker.com/v2/namespaces/{namespace}/repositories/{image}/tags?page={page}"
    
    while flip_flag:
        
        try:
            content=utils.get_url(url)
            for result in content['results']:
                tags.append(result['name'])
            if content['next']:# the next page exists
                url=content['next']
            else:
                flip_flag=False
        except:
            logging.info(f"Image {namespace}/{image} get wrong resp while getting tags; retrying; URL is https://hub.docker.com/v2/namespaces/{namespace}/repositories/{image}/tags?page={page}")
    logging.info(f"Image {namespace}/{image} has the following tags: {tags}")
    return tags

def get_images_by_tag(namespace,image,tag)->list[dict]:
    """
    To obtain information on each layer of an image with a specified tag
    by https://hub.docker.com/v2/repositories/library/ubuntu/tags/18.04/images
    """
    url=f"https://hub.docker.com/v2/repositories/{namespace}/{image}/tags/{tag}/images"
    
    max_retries,retry=5,0
    while retry<max_retries:
        
        try:
            content=utils.get_url(url)
            result=list()
            for image_obj in content:
                # For each image with this tag
                tmp={}
                tmp['overall_size']=image_obj['size']
                tmp['last_pushed']=image_obj['last_pulled']
                tmp['last_pulled']=image_obj['last_pulled']
                tmp['architecture']=image_obj['architecture']
                tmp['variant']=image_obj['variant']
                if 'digest' not in image_obj:
                    logging.info(f"{namespace}/{image}:{tag} is empty")
                    tmp['digest']=None
                else:
                    tmp['digest']=image_obj['digest']
                if 'os' not in image_obj:
                    logging.info(f"{namespace}/{image}:{tag} has no os")
                    tmp['os']=None
                else:
                    tmp['os']=image_obj['os']
                if "layers" not in image_obj:
                    logging.info(f"{namespace}/{image}:{tag} has no avaliable layers")
                else:
                    tmp['layers']=image_obj['layers']
                result.append(tmp)
            break
        except:
            if retry==max_retries:
                logging.exception(f"Image {namespace}/{image}:{tag} get wrong resp while getting building history; retrying {retry}")
                break
            logging.warning(f"Image {namespace}/{image}:{tag} get wrong resp while getting building history; retrying {retry}; URL is https://hub.docker.com/v2/repositories/{namespace}/{image}/tags/{tag}/images")
            retry+=1
    return result







    

    
