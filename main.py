# aiogram
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import Router
# asyncio
import asyncio
# requests
import requests
# os
import os
# dotevn
from dotenv import load_dotenv
# project

# Default setting project
load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

if API_TOKEN is None:
    raise ValueError('API_TOKEN не встановлено в оточенні або файлі .env')

if CHANNEL_ID is None:
    raise ValueError('CHANNEL_ID не встановлено в оточенні або файлі .env')

admin_ids_str = os.getenv('ADMIN_IDS', '')

if admin_ids_str:
    # завантажуємо ADMIN_IDS з файлу .env і перетворюємо його на список цілих чисел.
    ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS').split(',')))
else:
    ADMIN_IDS = []

# Перевірка чи правильно завантажується ADMIN_IDS з .env
print(f'Loaded ADMIN: {ADMIN_IDS}')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
admin_router = Router()

dp.include_router(admin_router)


# перевіряємо, чи є user_id в списку адміністраторів, який зберігається в ADMIN_IDS
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


# Code
@dp.message(CommandStart())
async def start_bot(message: Message):
    user_id = message.from_user.id
    if is_admin(user_id):
        await message.answer(f'Привіт {message.from_user.first_name}, я пересилаю повідомлення, які ти мені напишиш, і відправляю їх в телеграм канал\n{CHANNEL_ID}')
        all_message()
    else:
        await message.answer(f'У вас немає прав доступу до бота\nYour User ID: {user_id}')


@admin_router.message()
async def all_message(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    message_text = message.text
    if is_admin(user_id):
        # Пересилаємо повідомлення в канал
        await bot.send_message(CHANNEL_ID, f'{message_text}')
        # Відповідаємо користувачу
        await message.answer(f'Chat ID: {chat_id}\nUser ID:{user_id}\n\nMessage: {message_text}')
    else:
        await message.answer('Нажаль, ваш обліковий запис не має достатніх прав для доступу до функцій цього бота.\n\n'
                             'Якщо ви вважаєте, що це помилка, зверніться до адміністратора для отримання прав доступу.\n\n'
                             f'Адміністратори:\n(З\'явиться в майбутньому)')                             

# В майбутньому добавити SQL де будуть імена усіх адміністраторів

# Start
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
