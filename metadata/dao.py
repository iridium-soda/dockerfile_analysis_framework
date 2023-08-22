"""
Here implements operations about mongodb backends
"""
import pymongo
import logging
import sys 
PORT="27017"
BINDIP="127.0.0.1"

class database(object):
    def __init__(self,prefix,index):
        client = pymongo.MongoClient("mongodb://"+BINDIP+":"+PORT)
        self.db = client["analysis_db"] # NOTE: change it to read db after testing
        collection_path="_".join(["metadatas",prefix,index])
        self.collection = self.db[collection_path]

    def add(self,result:dict,index:int,image_nums:int):
        """
        To insert one result. No verification applied.
        """
        try:
            resp = self.collection.insert_one(result)
            if resp:
                logging.debug(f"[{index}/{image_nums}] Image {result['namespace']}/{result['image_name']} has been saved as {resp.inserted_id}")
            else:
                logging.exception(f"[{index}/{image_nums}] Image {result['image_name']} has NOT been saved")
        except Exception as e:
            print("Database IO exception: ",e)
        return resp.inserted_id

    def if_exist(self,namespace:str,image_name:str):
        return bool(self.collection.find_one({"namespace":namespace,"image_name":image_name}))