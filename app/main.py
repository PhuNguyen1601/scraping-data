from threading import Thread

import uvicorn
from server.app import schedule_scraping

if __name__ == "__main__":
    thread = Thread(target=schedule_scraping)
    thread.start()
    uvicorn.run("server.app:app", host="127.0.0.1", port=3000, reload=True)