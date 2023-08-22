"""
Getting image name, created date, update date, layers' history, layer size, short description, full description for each digest. Maybe docekrfile?
"""

import sys
import os

import logging
import proxy
from crawler import do_crawling

usage = """
Usage:
Getting image name, created date, update date, layers' history, layer size, short description, full description for each digest in .csv
metadata_crawler.py <path_to_images_list>
e.g. metadata_crawler.py results/all_images_a.list
"""


def main():
    if len(sys.argv) != 2:
        print(usage)
    else:
        # Check the validity of the input file path
        # Should be all_images_[prefix]_[index].list
        try:
            prefix, index = sys.argv[1].split(".")[-2].split("_")[-2:]
            logging.info("Get input info:", prefix, index)
        except:
            logging.exception("Invaild input path", sys.argv[1])



        # Combine log path
        log_path = "./logs/meta/meta_logs_" + prefix + "_" + index + ".log"
        if os.path.exists(log_path):  # Remove existed log file
            os.remove(log_path)
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format="[%(levelname)s]%(asctime)s : %(message)s",
            datefmt="%m-%d %H:%M:%S",
        )

        do_crawling(sys.argv[1], prefix, index)
        print(f"program for {sys.argv[1]} exited")
        logging.info(f"[SUCCESS] program for {sys.argv[1]} exited")


if __name__ == "__main__":
    main()
