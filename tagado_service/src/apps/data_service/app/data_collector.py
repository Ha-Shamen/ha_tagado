import datetime
import random
import requests
import json
from mongo_service import MongoService

def get_data(get_users: bool):
    mongo_service = MongoService()

    if get_users:
        r = requests.get("https://jsonplaceholder.typicode.com/users/")
        users_data = json.loads(r.text)
        mongo_service.insert_users(data=users_data)

    r = requests.get("https://jsonplaceholder.typicode.com/posts/")
    data = json.loads(r.text)
    max_id = mongo_service.find_max_id()
    
    data_with_new_id = [{**data_item, 
                         "_id": data_item["id"],
                         "insert_date": generate_random_date()
                         } 
                        for data_item in data if int(data_item["id"]) > max_id]
    
    data_to_insert = data_with_new_id[:10]
    if len(data_to_insert) > 0:
        mongo_service.insert_posts(data_to_insert)

        for post in data_to_insert:
            r = requests.get(f'https://jsonplaceholder.typicode.com/comments?postId={post["id"]}')
            comments_data = json.loads(r.text)
            if len(comments_data) > 0:
                comments_data_with_new_id = [{**comments_data_item, 
                         "_id": comments_data_item["id"]
                         } 
                        for comments_data_item in comments_data]
                mongo_service.insert_comments(comments_data_with_new_id)

def generate_random_date() -> datetime.datetime:
    start_date = datetime.datetime(2023, 1, 1)
    end_date   = datetime.datetime(2023, 5, 30)
    num_days   = (end_date - start_date).days
    rand_days   = random.randint(1, num_days)
    random_date = start_date + datetime.timedelta(days=rand_days)
    return random_date