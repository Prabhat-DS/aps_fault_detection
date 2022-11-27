import pymongo
import pandas as pd
import json

# Provide the mongodb localhost url to connect python to mongodb.
client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

data_path="/config/workspace/aps_failure_training_set1.csv"
dataBase_name = "aps"
collection_name = 'sensor'

if __name__ == "__main__":
    df = pd.read_csv(data_path)
    print(f"Rows and columns: {df.shape}")


    # convert data frame in .json formet so that we can dump these data into mongos DB
    df.reset_index(drop=True,inplace=True)

    json_record= list(json.loads(df.T.to_json()).values())
    print(json_record[0])

    # insert converted json_record  to mongodb
    client[dataBase_name][collection_name].insert_many(json_record)