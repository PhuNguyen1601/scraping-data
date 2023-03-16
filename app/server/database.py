import json
import os

import motor.motor_asyncio
from bson.objectid import ObjectId
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

path_mongodb = os.getenv('CONN_MONGODB')
path_data_scraping = os.getenv('PATH_DATA_SCRAPING')

MONGO_URI = path_mongodb
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client.backend
article_collection = database.get_collection("articles")
user_collection = database.get_collection("users")


def article_helper(article):
    return {
        "id": str(article["_id"]),
        "title": article["title"],
        "content": article["content"],
        "author": article["author"],
        "comment": article["comment"],
        "image": article["image"],
        "keywords": list(article["keywords"]),
    }



# Retrieves all the articles in the database
async def retrieve_articles():
    articles = []
    async for article in article_collection.find():
        articles.append(article_helper(article))
    return articles


# Add a new article to database
async def add_article(article_data: dict) -> dict:
    article = await article_collection.insert_one(article_data)
    new_article = await article_collection.find_one({"_id": article.inserted_id})
    return article_helper(new_article)

## Add multiple new article to database
async def insert_data_from_json():
    with open(path_data_scraping) as f:
        data = json.load(f)
        result = await article_collection.insert_many(data)
        articles = []
        async for article in article_collection.find():
            articles.append(article_helper(article))
        return articles



# Retrieve a article with matching id
async def retrieve_article(id: str) -> dict:
    article = await article_collection.find_one({"_id": ObjectId(id)})
    if article:
        return article_helper(article)


# Update a article with matching ID
async def update_article(id: str, data: dict):
    if len(data) < 1:
        return False
    article = await article_collection.find_one({"_id": ObjectId(id)})
    if article:
        updated_article = await article_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_article:
            return True
        return False

# Delete a article from database
async def delete_article(id: str):
    article = await article_collection.find_one({"_id": ObjectId(id)})
    if article:
        await article_collection.delete_one({"_id": ObjectId(id)})
        return True 
    
def user_helper(user):
    return {
        "id": str(user["_id"]),
        "full_name": user["full_name"],
        "user_name": user["user_name"],
        "password": user["password"],
        "address": user["address"],
        "avatar": user["avatar"],
    }


# Retrieves all the users in the database
async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


# Add a new user to database
async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

# Add multiple new user to database
async def insert_data_from_json(file_path):
    with open(file_path) as f:
        data = json.load(f)
        user_collection.insert_many(data)
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


# Retrieve a user with matching id
async def retrieve_user(id: str) -> dict:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)


# Update a user with matching ID
async def update_user(id: str, data: dict):
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False

# Delete a user from database
async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True 