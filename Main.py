# main.py
import logging
import requests
from aiogram import Bot, Dispatcher, types, executor
import os

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
PICWISH_API_KEY = os.getenv("PICWISH_API_KEY")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("Привет! Отправь мне фото татуировки, и я покажу, как она может выглядеть без неё.")

@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    await message.reply("Фото получено! Удаляю татуировку...")

    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file = await bot.download_file(file_info.file_path)

    # Отправляем на PicWish
    url = "https://api.picwish.com/v1/remove-mark"
    headers = {"X-API-KEY": PICWISH_API_KEY}
    files = {"file": file}

    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        result = response.json()
        image_url = result["data"]["url"]
        await message.answer_photo(photo=image_url)
    else:
        await message.reply("Произошла ошибка при обработке фото. Попробуй позже.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
