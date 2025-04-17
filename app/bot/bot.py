from aiogram import Bot
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('TELEGRAM_BOT_TOKEN')

bot = Bot(token=token)
