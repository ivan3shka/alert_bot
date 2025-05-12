import asyncio
import os
from collections import deque
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command

from config import BOT_TOKEN, CHAT_ID
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Храним последние ссылки для избежания повторной отправки
set_with_links = deque(maxlen=20)

async def check_new_links(bot):
    URL = 'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA?place=0-11'
    print('Запуск Selenium...')

    chrome_options = Options()
    # Режим без графического интерфейса (headless)
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--window-size=1920,1080')

    # Установка chromedriver через webdriver_manager
    # Установка chromedriver через webdriver_manager
    driver_path = ChromeDriverManager().install()
    # Определяем директорию, где лежит chromedriver
    driver_dir = os.path.dirname(driver_path)
    # Составляем путь к исполняемому файлу chromedriver
    executable = os.path.join(driver_dir, "chromedriver")
    # Устанавливаем права на исполняемый файл
    os.chmod(executable, 0o755)
    print("Driver path:", driver_path)
    print("Executable path:", executable)

    service = Service(executable)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(URL)
        # Ожидаем появления элемента (увеличьте таймаут, если требуется)
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'NewBuildingItem__ImageWrapper-sc-o36w9y-2'))
        )

        new_building_links = driver.find_elements(By.CLASS_NAME, 'NewBuildingItem__ImageWrapper-sc-o36w9y-2')
        new_found = False

        for link in new_building_links:
            href = link.get_attribute('href')
            if href and href not in set_with_links:
                new_found = True
                set_with_links.append(href)

        if new_found:
            text = (f'Вышла новая публикация на <a href="{URL}">сайте!</a>\n'
                    f'(наш.дом.рф)')
            await bot.send_message(CHAT_ID, text)
    finally:
        driver.quit()

async def main_nashdom():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    @dp.message(Command('start'))
    async def start_handler(message):
        await message.answer('Привет!\nБот начинает работу!')

    try:
        while True:
            await check_new_links(bot)
            # Пауза в 24 часа (60*60*24 секунд)
            await asyncio.sleep(60)
    finally:
        await bot.session.close()

