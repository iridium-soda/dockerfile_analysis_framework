"""
Here implements operations about mongodb backends
"""
import pymongo
import logging
import sys 
PORT="27017"
BINDIP="127.0.0.1"

class database(object):
    def __init__(self):
        client = pymongo.MongoClient("mongodb://"+BINDIP+":"+PORT)
        self.db = client["analysis_db"] # NOTE: change it to read db after testing
        collection_path="metadatas"+sys.argv[1].split('.')[0][-1]
        self.collection = self.db[collection_path]

    def add(self,result:dict):
        """
        To insert one result. No verification applied.
        """
        try:
            resp = self.collection.insert_one(result)
            if resp:
                logging.debug(f"Image {result['namespace']}/{result['image_name']} has been saved as {resp.inserted_id}")
            else:
                logging.exception(f"Image {result['image_name']} has NOT been saved")
        except Exception as e:
            print("Database IO exception: ",e)
        return resp.inserted_id

