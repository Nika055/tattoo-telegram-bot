from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os

# Получаем токен из переменных окружения
API_TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Отправь мне фото своей татуировки, и я покажу, как она может выглядеть без неё.")

@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    await message.reply("Фото получено! В ближайшее время я научусь удалять тату — следи за обновлениями.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
