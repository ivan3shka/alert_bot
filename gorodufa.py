import asyncio
import aiohttp
from bs4 import BeautifulSoup
from config import URL_GORODUFA, CHAT_ID, BOT_TOKEN
from aiogram import Bot
from collections import deque

SEARCH_TITLE = 'О разработке проекта планировки и проекта межевания территории'

file_url_check = deque(maxlen=11)


def add_file_url(url):
    """Добавляет ссылку в очередь"""
    file_url_check.append(url)


async def fetch_html(url: str) -> str:
    """Загружает HTML-страницу"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def parse_and_download(bot: Bot):
    """Парсит сайт, ищет нужный заголовок и отправляет ссылку в Telegram"""
    global file_url_check

    html = await fetch_html(URL_GORODUFA)
    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.find_all(['h1', 'h2', 'h3'])

    for article in articles:
        if SEARCH_TITLE in article.get_text(strip=True):

            next_sibling = article.find_next('a', href=True)
            while next_sibling:
                if 'Скачать' in next_sibling.text and next_sibling['href'].endswith('.pdf'):
                    file_url = next_sibling['href']

                    if not file_url.startswith('http'):
                        file_url = 'https://gorodufa.ru' + file_url

                    if file_url in file_url_check:
                        return

                    add_file_url(file_url)

                    await bot.send_message(CHAT_ID,
                                           f'🆕 Найдена новая публикация: "{article.get_text(strip=True)}"'
                                           f'\nна {URL_GORODUFA}! '
                                           f'[Скачать PDF]({file_url})',
                                           parse_mode='Markdown')
                    async def send_reminder():
                        await asyncio.sleep(10)
                        await bot.send_message(
                            CHAT_ID,
                            '⏰ Проверьте сайт https://gorodufa.ru/docs/ '
                            '— сегодня могло выйти ещё одно объявление.'
                        )

                    asyncio.create_task(send_reminder())
                    return
                next_sibling = next_sibling.find_next('a', href=True)


async def main_gorodufa():
    """Основной цикл проверки сайта"""
    bot = Bot(token=BOT_TOKEN)

    try:
        while True:
            await parse_and_download(bot)
            await asyncio.sleep(60*60*24*3)
    finally:
        await bot.session.close()
