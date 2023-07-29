"""
Getting image name, created date, update date, layers' history, layer size, short description, full description for each digest. Maybe docekrfile?
"""

import sys
import os


import logging

from crawler import do_crawling

usage="""
Usage:
Getting image name, created date, update date, layers' history, layer size, short description, full description for each digest in .csv
metadata_crawler.py <path_to_images_list>
e.g. metadata_crawler.py results/all_images_a.list
"""


def main():

    if len(sys.argv)!=2:
        print(usage)
    else:
        # Combile log path
        log_path="./logs/meta/meta_logs_"+sys.argv[1].split('.')[0][-1]+".log"
        if os.path.exists(log_path): # Remove existed log file
            os.remove(log_path)
        logging.basicConfig(filename=log_path, level=logging.INFO,format='[%(levelname)s]%(asctime)s : %(message)s',datefmt="%m-%d %H:%M:%S")

        do_crawling(sys.argv[1])
        print(f"program for {sys.argv[1]} exited")
        logging.INFO(f"[SUCCESS] program for {sys.argv[1]} exited")

if __name__=="__main__":
    main()
    