import pandas as pd
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.config import mongo_client
import os, sys

def get_collection_as_dataframe(database_name:str, collection_name:str)-> pd.DataFrame:
    """
    This funtion return collection as data fram
    database_name: database name
    collection_name: collection name
    ================================================
    return pandas dataframe of a collection
    """
    try:
        logging.info(f"reading data from database: {database_name} and collection: {collection_name}")
        df= pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        loging.info(f"Found column: {df.columns}")
        if "_id" in df.columns:
            logging.info(f"droping column: _id")
            df = df.drop("_id", axis=1)
        logging.info(f"row and columns in df: {df.shape}")
        return df 
    except Exception as e:
        raise SensorException(e, sys)