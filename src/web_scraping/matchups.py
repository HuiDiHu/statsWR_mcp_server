import asyncio
from bs4 import BeautifulSoup
import requests
import time

# MAY HAVE TO UNINSTALL .venv AND REINSTALL, THEN RUN REQUESTS BELOW
# uv pip install .
# uv pip install requests
# uv pip install beautifulsoup4
# uv pip install lxml

# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-next-siblings-and-find-next-sibling

def scrape_website(url):
    req = requests.get(url)
    return req.text

async def scrape_matchups(champion_name):
    url = f'https://wildriftcounter.com/champions/{champion_name}/'

    html_text = await asyncio.to_thread(scrape_website, url)
    soup = BeautifulSoup(html_text, 'lxml')

    result = []
    gallery_counter = 1

    valid_roles = {'Top':1, 'Jungler':2, 'Mid':3, 'Bot':4, 'Bottom':4, 'Support':5}
    necessary_paragraph = soup.find_all('p', class_="has-text-align-center")
    for paragraph in necessary_paragraph:
        if paragraph.text in valid_roles:

            while not soup.find('div', id = f'gallery-{gallery_counter}') and gallery_counter < 20:
                gallery_counter += 1 # APPARENTLY GALLERY DOESN'T ALWAYS START AT 1

            if gallery_counter == 20:
                result.append('there was an error scraping')
                break

            counters_container = soup.find('div', id = f'gallery-{gallery_counter}')
            gallery_counter += 1
            counters_figcaptions = counters_container.find_all('figcaption')
            good_matchups_container = soup.find('div', id = f'gallery-{gallery_counter}')
            gallery_counter += 1
            good_matchups_figcaptions = good_matchups_container.find_all('figcaption')
            counters = list(map(lambda x: x.a.text, counters_figcaptions))
            good_matchups = list(map(lambda x: x.a.text, good_matchups_figcaptions))

            parent = good_matchups_container.find_parent('div').find_parent('div')
            sibling = parent.find_next_sibling()
            info = []
            while sibling and sibling.name == 'p': # returns 'p' 
                info.append(sibling.text)
                sibling = sibling.find_next_sibling()
            if info and info[-1] in valid_roles:
                info.pop()
                
            data = {'_role_id':valid_roles[paragraph.text], 'counters':counters, 'good_matchups':good_matchups, 'counter_strategy':" ".join(info)}
            result.append(data)

    return result

if __name__ == '__main__':
    matchups = asyncio.run(scrape_matchups('dr-mundo'))
    print(matchups)

__all__ = [
    "scrape_matchups",
]
