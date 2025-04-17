from app.handlers import router
from aiogram import Dispatcher
from app.bot.bot import bot
from app.database.models import async_main
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
async def main():
    try:
        await async_main()
    except Exception as e:
        print(e)
    dp = Dispatcher()
    dp.include_router(router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped")
