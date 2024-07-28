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
from scrape_rozetka import scrape_rozetka


# Default setting project
load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
ADMIN_IDS = os.getenv('ADMIN_IDS')
ADMIN_NAME = os.getenv('ADMIN_NAME')

if API_TOKEN is None:
    raise ValueError('API_TOKEN не встановлено в оточенні або файлі .env')

if CHANNEL_ID is None:
    raise ValueError('CHANNEL_ID не встановлено в оточенні або файлі .env')

if ADMIN_NAME is None:
    raise ValueError('ADMIN_NAME не встановлено в оточенні або файлі .env')

admin_ids_str = os.getenv('ADMIN_IDS', '')

admin_name_str = os.getenv('ADMIN_NAME', '')

if admin_ids_str:
    # завантажуємо ADMIN_IDS з файлу .env і перетворюємо його на список цілих чисел.
    ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS').split(',')))
else:
    ADMIN_IDS = []

if admin_name_str:
    ADMIN_NAME = list(map(str, os.getenv('ADMIN_NAME').split(',')))
else:
    ADMIN_NAME = []

# Показати адмінів з ADMIN_IDS з .env
print(f'Loaded ADMIN: {ADMIN_IDS} {ADMIN_NAME}')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# перевіряємо, чи є user_id в списку адміністраторів, який зберігається в ADMIN_IDS
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

# перевіряємо, чи є user_name в списку адміністраторів, який зберігається в ADMIN_NAME
def admin_name(user_name: str) -> bool:
    return user_name in ADMIN_NAME


# Code
@dp.message(CommandStart())
async def start_bot(message: Message):
    user_id = message.from_user.id
    if is_admin(user_id):
        await message.answer(f'Привіт {message.from_user.first_name}, я пересилаю повідомлення, які ти мені напишиш, і відправляю їх в телеграм канал\n{CHANNEL_ID}')
    else:
        await message.answer(f'У вас немає прав доступу до бота\nYour User ID: {user_id}')


@dp.message(Command(commands='help'))
async def send_help(message: Message):
    await message.reply('Команди бота:\n\n'
                        '/start - Запуск бота\n\n'
                        '/get_notebook - Отримати список ноутбуків з "Rozetka"\n\n'
                        '/get_my_id - Отримати своє id\n\n')


@dp.message(Command(commands='get_notebook'))
async def get_notebook_info(message: Message):
    title, description, url = await scrape_rozetka()
    response = (f'Назва: {title}\n\n'
                f'Опис: {description}\n\n'
                f'Посилання: {url}')
    await message.reply(response)


@dp.message()
async def all_message(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    message_text = message.text
    if is_admin(user_id):
        # Пересилаємо повідомлення в канал
        await bot.send_message(CHANNEL_ID, f'{message_text}')
        # Відповідаємо користувачу
        await message.answer(f'Chat ID: {chat_id}\n\n'
                             f'Message:\n\n{message_text}')
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
