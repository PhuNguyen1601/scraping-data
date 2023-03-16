import asyncio
import json
import os

import aiohttp
import nltk
from bs4 import BeautifulSoup
from dotenv import find_dotenv, load_dotenv
from rake_nltk import Rake

nltk.download('stopwords')

load_dotenv(find_dotenv())

path_data_scraping = os.getenv('PATH_DATA_SCRAPING')
default_header = os.getenv('DEFAULT_HEADER')
path_scraping = os.getenv('PATH_SCRAPING')

DEFAULT_HEADER = {
    "User-Agent": f"{default_header}"
}


dir_path = os.path.dirname(os.path.realpath(__file__))
file_name = os.path.join(dir_path, path_data_scraping)
##
async def get_soup(session, url):
    async with session.get(url, headers=DEFAULT_HEADER, timeout=15) as response:
        text = await response.text()
        soup = BeautifulSoup(text, "lxml")
        return soup
##
async def get_article_data(session, article):
    data = {
        "title": None,
        "content": None,
        "author": None,
        "comment": None,
        "image": None,
        "key_words": []
    }
    title_elem = article.find("span", {"class": "titleline"}).find("a")
    if title_elem is not None:
        title = title_elem.text.strip()
        link = title_elem['href']
    else:
        title = 'N/A'
    next_article = article.find_next_sibling("tr")
    author_elem = next_article.find('a', class_='hnuser')
    if author_elem is not None:
        author = author_elem.text.strip()
    else:
        author = 'N/A'
    links = next_article.find_all("a")
    comments = 0
    for link_cmt in links:
        if "item?id=" in link_cmt["href"]:
            try:
                comments = int(link_cmt.text.split()[0])
                break
            except ValueError:
                pass
    try:
        async with session.get(link, headers=DEFAULT_HEADER, timeout=5) as sub_response:
            sub_text = await sub_response.text()
            sub_page = BeautifulSoup(sub_text, "html.parser")
            img_tags = sub_page.find_all("img")
            if img_tags:
                img_tags.sort(key=lambda x: (x.get("width", 0), x.get("height", 0)), reverse=True)
                largest_img = img_tags[0]["src"]
            else:
                largest_img = None
            paragraphs = [p.text.strip() for p in sub_page.find_all("p")]
            content = "\n".join(paragraphs)
            key_words = get_key_word(content)
            data["title"] = title
            data["content"] = content
            data["author"] = author
            data["comment"] = comments
            data["image"] = largest_img
            data["key_words"] = key_words
            
    except:
        data["title"] = title
        data["content"] = "N/A"
        data["author"] = author
        data["comment"] = comments
        data["image"] = None
        data["key_words"] = []

    return data
##
def get_key_word(content):
    r = Rake()
    r.extract_keywords_from_text(content)
    for rating, keyword in r.get_ranked_phrases_with_scores():
        if rating > 5:
            return keyword
        else:
            return None
##
async def scrape_articles():
    articles = []
    page = 1
    url = path_scraping
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(10)
        queue = asyncio.Queue()
        while True:
            try:
                soup = await get_soup(session, url)
            except aiohttp.ClientError:
                break
            for article in soup.select("tr.athing"):
                await queue.put(article)
            more_link = soup.select_one("a.morelink")
            if more_link:
                page += 1
                url = f"{path_scraping}?p={page}"
            else:
                break
        tasks = []
        while not queue.empty():
            article = await queue.get()
            async with semaphore:
                task = asyncio.create_task(get_article_data(session, article))
                tasks.append(task)
        articles = await asyncio.gather(*tasks)
    return articles

##
def write_to_file(data, filename):
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            old_data = json.load(f)
        if isinstance(old_data, list):
            old_data.extend(data)
            data = old_data
        else:
            print(f"Error: {filename} does not contain a list of data.")
            return
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error writing data to {filename}: {e}")


##
def scraping():
# if __name__ == "__main__":
    try:
        articles = asyncio.run(scrape_articles())
        write_to_file(articles, file_name)
    except Exception as e:
        print("An error occurred:", e)
    
