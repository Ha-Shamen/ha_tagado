import os
from typing import List
from pymongo import MongoClient


class MongoService:

    def __init__(self, client: MongoClient = None) -> None:

        mongo_connection = \
                os.environ.get("MONGOSERVICE") or \
                "mongodb://mongo:27017/testdb"
        self.client = client or MongoClient(mongo_connection)
        self.db = self.client['tagado']
        self.posts_collection = "tagado_post_items"
        self.comments_collection = "tagado_comments_items"
        self.users_collection = "tagado_users_items"
        self.db[self.posts_collection]    
        self.db[self.comments_collection]
        self.db[self.users_collection]
        self.db[self.comments_collection].create_index([( "body", "text" )])
        self.db[self.users_collection].create_index("id", unique = True)
    
    def insert_posts(self, data: List = None) -> None:
        
        collection = self.db.get_collection(self.posts_collection)
        collection.insert_many(data)

    def insert_comments(self, data: List = None) -> None:
        
        collection = self.db.get_collection(self.comments_collection)
        collection.insert_many(data)
    
    def insert_users(self, data: List = None) -> None:
        
        collection = self.db.get_collection(self.users_collection)
        collection.insert_many(data)

    def find_max_id(self) -> int:
        collection = self.db.get_collection(self.posts_collection)
        res = collection.find()   
        res_as_list = list(res)
        max_id = -1
        if len(res_as_list) > 0:
            max_id = max(res_as_list, key=lambda x: x['id'])["id"]
        return max_id