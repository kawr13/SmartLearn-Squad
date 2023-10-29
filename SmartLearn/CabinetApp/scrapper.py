from bs4 import BeautifulSoup as bs
import asyncio
import aiohttp
from icecream import ic


URL = 'https://ya.ru/search/?text='

async def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                ic(response.status)
                return await response.text()
            ic(response.status)


async def parse_html(html):
    listen_text = []
    soup = bs(html, 'lxml')
    items = soup.find_all('a')
    for item in items:
        description = ic(item.text)
        web = ic(item.get('href'))
        sps = {'description': description, 'web': web}
        listen_text.append(sps)
    return listen_text


async def starting_pars(answer: str):
    new_adris = f'https://ya.ru/search/?text={answer}'
    ic(new_adris)
    html = await asyncio.create_task(get_html(new_adris))
    res = await asyncio.create_task(parse_html(html))
    return res

if __name__ == '__main__':
    answer = 'python'
    asyncio.run(main(answer))

