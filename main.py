# aiogram
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import Router
# asyncio
import asyncio
# os
import os
# dotevn
from dotenv import load_dotenv
# project


# Default setting project
load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

if API_TOKEN is None:
    raise ValueError('API_TOKEN is not set in the environment or .env file')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

dp.include_router(router)


# Code
@dp.message(CommandStart())
async def start_bot(message: Message):
    await message.answer(f'{message}')


# Start
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
