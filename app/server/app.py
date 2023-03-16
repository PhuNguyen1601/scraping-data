
import time

import schedule
from fastapi import FastAPI

from .database import insert_data_from_json
from .routes.article import router as ArticleRouter
from .routes.user import router as UserRouter
from .scraping import scraping

app = FastAPI()

app.include_router(ArticleRouter, tags=["Articles"], prefix="/article")
app.include_router(UserRouter, tags=["Users"], prefix="/user")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}


def scrape_articles():
    print('Scraping...!')
    scraping()
    insert_data_from_json()
    return "Scraping successfully!"

def schedule_scraping():
    while True:
        schedule.run_pending()
        time.sleep(1)
        
schedule.every(60).minutes.do(scrape_articles)
