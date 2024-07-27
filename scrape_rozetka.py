import aiohttp
from bs4 import BeautifulSoup

async def scrape_rozetka():
    URL = 'https://rozetka.com.ua/ua/notebooks/c80004/'

    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            page_content = await response.text()

    soup = BeautifulSoup(page_content, 'html.parser')

    # пошук першого ноутбуку
    post = soup.find('li', class_='catalog-grid__cell catalog-grid__cell_type_slim ng-star-inserted')

    if post:
        title = post.find('a', class_='goods-tile__heading').text.strip()
        description = post.find('div', class_='goods-tile__availability goods-tile__availability--available ng-star-inserted').text.strip()
        url = post.find('a', class_='goods-tile__heading', href=True)['href'].strip()
        
        return title, description, url
    else:
        return 'Немає title', 'Немає description', 'Немає url'
