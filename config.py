import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
if BOT_TOKEN is None:
    exit('BOT_TOKEN отсутствует в переменных окружения')

URL_GORODUFA = 'https://gorodufa.ru/docs/'

DEFAULT_COMMANDS = (
    ('start', 'Начать'),
)
