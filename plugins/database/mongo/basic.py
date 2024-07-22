from os import getenv
from re import compile
from typing import Union
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv(), override=True)
MONGO_SERVER = getenv("MONGO_SERVER")
MONGO_DATABASE_NAME = getenv("MONGO_DATABASE_NAME")


class MongoBasic:

    def __init__(self, database_name: str = None) -> None:
        """
        Set your `database_name` or uses .env by default.
        """
        self.client = MongoClient(MONGO_SERVER)
        self.db = self.client[database_name or MONGO_DATABASE_NAME]

    def collection_names(self):
        """
        Returns
        -------
        List of collection names exists in selected database.
        """
        return self.db.list_collection_names()

    def reset_database(self) -> bool:
        """
        Fully delete and reset databases
        """
        try:
            collections = self.db.list_collection_names()
            print(f"<MongoBasic>:::Deleting collections: {collections}")
            for collection in collections:
                self.db[collection].delete_many({})
            return True
        except Exception as Error:
            print(f"<MongoBasic>:::Error in reset_database()\n     └─────{Error}\n")
            return False

    def reset_collection(self, collection_name:str) -> bool:
        try:
            self.db[collection_name].delete_many({})
            return True
        except Exception as Error:
            print(f"<MongoBasic>:::Error in reset_database()\n     └─────{Error}\n")
            return False

    def collection_exist(self, collection_name:str) -> bool:
        """
        Returns
        -------
        `bool`: `True` if collection exists in the database, otherwise `False`.
        """
        return collection_name in self.db.list_collection_names()

    def drop_collection(self, collection_name:str = None, pattern:str = None) -> bool:
        """
        Drop a single collection using `collection_name` or RegEx `pattern`.
            <At least one of the arguments must be filled> 
        """
        try:
            if pattern:
                regex = compile(pattern)
                for coll_name in self.db.list_collection_names():
                    if regex.match(coll_name):
                        self.db[coll_name].drop()
                        return True
                    
                return False

            else:
                self.db[collection_name].drop()
                return True
        except Exception as Error:
            print(f"<MongoBasic>:::Error in drop_collection()\n     └─────{Error}\n")
            return False

    def drop_database(self, database_name:str) -> bool:
        """
        Drop a database using it's name.
        """
        try:
            self.client.drop_database(database_name)
            return True
        except Exception as Error:
            print(f"<MongoBasic>:::Error in drop_database()\n     └─────{Error}\n")
            return False

    def insert_data(self, collection_name:str, data:Union[list[dict], dict], show_errors:bool = False) -> bool:
        """
        Inserts Data into the `collection_name`.
        """
        try:
            if type(data) == dict:
                self.db[collection_name].insert_one(data)
            elif type(data) == list:
                self.db[collection_name].insert_many(data)
            return True
        except Exception as Error:
            if show_errors:
                print(f"<MongoBasic>:::Error in insert_data()\n     └─────{Error}\n")
            return False

    def load_data(self, collection_name:str, query={}, filter={}, limit=0, first:bool=False) -> Union[dict, list[dict]]:
        """
        Itrates over `collection` name.
        ## Parameters
            collection_name (`str`):
                <name> of database table
            query (`dict | {}`):
                mongo <query>:
                    `{"name": "juan"}`
            filter (`dict | {}`):
                mongo <filter>:
                    `{"_id": 0}` or `{"_id": 1}`
            limit (`int | 0`):
                Limits the number of results to be returned by the cursor,  A limit of 0 is equivalent to no limit.
        ## Returns
        ----------
        `dict` | list[`dict`]
        """
        try:
            if first:
                return self.db[collection_name].find_one(query, filter)
            else:
                return [col for col in self.db[collection_name].find(query, filter).limit(limit)]
        except Exception as Error:
            print(f"<MongoBasic>:::Error in load_data()\n     └─────{Error}\n")
            return dict()

    def update_data(self, collection_name:str, query:dict, value:dict, upsert=False) -> bool:
        """
        ## Parameters
            query (`dict` | `{}`):
                mongo <query>:
                    $where -> `{"name": "juan"}`
            value (`dict` | `{}`):
                mongo <value:dict>:
                    $set -> `{"name": "max"}`
        """
        try:
            self.db[collection_name].update_one(query, {'$set': value}, upsert=upsert)
            return True
        except Exception as Error:
            print(f"<MongoBasic>:::Error in update_data()\n     └─────{Error}\n")
            return False

    def push_data(self, collection_name:str, query:dict, value:dict) -> bool:
        """
        Append item to MongoDB document array without re-insertion.
        """
        try:
            if type(value) == dict:
                self.db[collection_name].update_one(query, {'$push': value})
            elif type(value) == list:
                self.db[collection_name].update_one(query, {'$push': {'$each': value}})
            return True
        except Exception as Error:
            print(f"<MongoBasic>:::Error in push_data()\n     └─────{Error}\n")
            return False

    def delete_data(self, collection_name:str, query={}, delete_many: bool = True) -> bool:
        """
        Deletes data from given `collection_name`.
        """
        try:
            if delete_many:
                self.db[collection_name].delete_many(query)
            else:
                self.db[collection_name].delete_one(query)
                
            return True
        
        except Exception as Error:
            print(f"<MongoBasic>:::Error in delete_data()\n     └─────{Error}\n")
            return False

    def create_unique_index(self, collection_name: str, key: str):
        self.db[collection_name].create_index(key, unique=True)
