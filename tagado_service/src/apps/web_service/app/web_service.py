import datetime
from fastapi import FastAPI
from .mongo_service import MongoService


app = FastAPI()
mongo_service = MongoService()

@app.get("/")
def read_all_posts():
    return mongo_service.get_all_posts()

@app.get("/post/")
def read_by_post_id(post_id: str):
    return mongo_service.get_by_post_id(post_id=post_id)

@app.get("/comments/")
def find_comments_by_post_id(post_id: str):
    return mongo_service.get_all_comments_by_post_id(post_id=post_id)

@app.get("/simple/")
def find_comments_by_post_id_simple(post_id: str):
    return mongo_service.get_all_comments_by_post_id_simple(post_id=post_id)

@app.get("/search/")
def find_comments_by_text(text: str):
    return mongo_service.get_all_comments_by_text(text=text)

@app.get("/dates/")
def count_posts_by_date_range(from_date: str, to_date: str):

    date_format = '%Y-%m-%d'
    try:
        dateObject = datetime.datetime.strptime(from_date, date_format)
        dateObject = datetime.datetime.strptime(to_date, date_format)
    except ValueError:
        return {
            "error": "Incorrect data format, should be YYYY-MM-DD"
        }

    return mongo_service.count_posts_by_date_range(from_date=from_date, to_date=to_date)

@app.put("/posts/")
def update_post(user_email: str, post_id: str, message: str):
    return mongo_service.update_post_message(user_email=user_email, post_id=post_id, message=message)
    