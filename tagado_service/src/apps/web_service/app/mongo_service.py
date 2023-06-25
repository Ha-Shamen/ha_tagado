import os
from typing import List, Dict, Text
import json
import requests
from pymongo import MongoClient
import datetime


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
       
    def get_all_comments_by_post_id(self, post_id: str) -> List:
        collection = self.db.get_collection(self.comments_collection) 
        res = collection.find({ "postId": int(post_id) })
        res_list = list(res)
        if len(res_list) > 0:  
            res_items = [item for item in res_list]
            comments = [item['body'] for item in res_items]
            return comments

        return []
    
    def get_all_comments_by_post_id_simple(self, post_id: int) -> List:
        r = requests.get(f'https://jsonplaceholder.typicode.com/comments?postId={post_id}')
        comments_data = json.loads(r.text)
        return comments_data
    
    def get_all_comments_by_text(self, text: str) -> List:
        collection = self.db.get_collection(self.comments_collection) 
        res = collection.find({ "$text": { "$search": text } })
        return str(list(res))
    
    def count_posts_by_date_range(self, from_date: str, to_date: str) -> Dict:
        from_datetime = datetime.datetime.strptime(from_date, 
                                                   "%Y-%m-%d")
        to_datetime = datetime.datetime.strptime(to_date, 
                                                   "%Y-%m-%d")
        collection = self.db.get_collection(self.posts_collection) 

        res = collection.count_documents({"insert_date": {
                                                "$gt": from_datetime,
                                                "$lt": to_datetime
                                            }})
        return {
            "documents_count": str(res)
        }

    def update_post_message(self, user_email: str, post_id: str, message: str) -> Dict:
        reject_reason = 'Post does not exist'
        collection = self.db.get_collection(self.posts_collection) 
        res = collection.find({ "id": int(post_id) })
        res_as_list = list(res)
        if len(res_as_list) > 0:
            # Expecting single post
            post_user_id = res_as_list[0]["userId"]
            users_collection = self.db.get_collection(self.users_collection)
            res_user = users_collection.find({ "id": int(post_user_id) })
            res_user_as_list = list(res_user)
            if len(res_user_as_list) > 0:
                # Expecting single user
                res_user_email = str(res_user_as_list[0]["email"])
                if user_email.lower() == res_user_email.lower():
                    # not sure if to update in web or locally 
                    # updating both
                    params = {
                        "id": int(post_user_id),
                        "body": message
                    }
                    r = requests.put(f'https://jsonplaceholder.typicode.com/posts/{post_id}',
                                     params=params)
                    
                    filter = { 'id': int(post_id) }
                    # Values to be updated.
                    newvalues = { "$set": { 'body': message } }
                    
                    # Using update_one() method for single
                    # updation.
                    collection.update_one(filter, newvalues)
                    return { "result": "post updated"}
                
                reject_reason = 'User is not permitted to update post'

            else:
                reject_reason = 'Post defined user does not exist'

        return {
            "reject_reason": reject_reason
        }
    
    def get_all_posts(self) -> Text:
        collection = self.db.get_collection(self.posts_collection)
        res = collection.find()   
        return str(list(res))
    
    def get_by_post_id(self, post_id: str) -> List:
        collection = self.db.get_collection(self.posts_collection) 
        res = collection.find({ "id": int(post_id) })
        res_list = list(res)
        return str(res_list)
    
if __name__ == '__main__':
    mongo = MongoService()