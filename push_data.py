import os
import sys
import json
import pandas as pd
import numpy as np
import pymongo
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca = certifi.where()

class Network_Data_Extract():

    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e, sys)
        
    def insert_data_mongo_db(self, records, database, collection):
        try:
            self.records = records
            self.database = database
            self.collection = collection

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)

            return len(self.records)

        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e, sys)
        
if __name__ == '__main__':
    FILE_PATH = r"C:\Users\Z0166121\Downloads\Network_Security\Network_Data\phisingData.csv"
    DATABASE = "NIKHIL_AI_Security"
    Collection = "NetworkData"

    network_obj = Network_Data_Extract()

    data_records = network_obj.csv_to_json_convertor(FILE_PATH)
    no_of_records = network_obj.insert_data_mongo_db(data_records, DATABASE, Collection)

    print(no_of_records)
    logging.info(no_of_records)