import asyncio
from bs4 import BeautifulSoup
import requests
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

# MAY HAVE TO UNINSTALL .venv AND REINSTALL, THEN RUN REQUESTS BELOW
# uv pip install .
# uv pip install requests
# uv pip install beautifulsoup4
# uv pip install lxml

# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-next-siblings-and-find-next-sibling

# 1. QUESTION: Why did gragas become so strong / why did his pickrate spike -> keep asking user for specific date.
# 2. MCP SERVER FUNCTION: Searches database for highest winrate/pickrate/banrate/rank gragas update, and then finds date of latest patch before that update.
# THIS REQUIRES A HASHMAP WITH DATES AS KEYS AND patch_id AS VALUES. TRAVERSE THE KEYS UNTIL UPDATE DATE (on statsWR) < PATCH DATE and then go back 1 index. RETURN
# THE APPROPRIATE PATCH_ID AND PASS IT TO THE WEB SCRAPING FUNCTION. (WE ONLY PAY ATTENTION TO PATCHES AFTER MAY 2024)
# 3. WEB SCRAPING FUNCTION: Use patch_id to web scrape the appropriate page.

def scrape_website(url):
    opts = Options()
    opts.add_argument("--headless")
    driver = webdriver.Firefox(options=opts)
    driver.implicitly_wait(10)
    driver.get(url)
    return driver.page_source

async def scrape_patch_by_id(patch_id):
    url = f'https://wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-{patch_id}/' # 6-1c

    html_text = await asyncio.to_thread(scrape_website, url)
    soup = BeautifulSoup(html_text, 'lxml')
    text = soup.find('main').div.div.text.split('Related Articles')[0]

    # with open('./stuff.txt', 'w', encoding='utf-8') as data:
    #     data.write(text)

    return text

if __name__ == '__main__':
    patch = asyncio.run(scrape_patch_by_id('6-1d'))
    print(patch)

__all__ = [
    "scrape_patch_by_id",
]
