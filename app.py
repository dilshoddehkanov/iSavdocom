import logging
import requests

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode

API_TOKEN = ''

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)


def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None


@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    unique_code = extract_unique_code(message.text)
    url = f'https://isavdo.com/api/spread/{unique_code}'

    r = requests.get(url)
    res = r.json()
    photoUrl = f'https://isavdo.com{res["data"]["photo"]}'
    # print(photoUrl)
    inlineKeyboard =InlineKeyboardMarkup()
    inlineKeyboard.row(
        InlineKeyboardButton('👨🏻‍💻 Buyurmat berish', url=f'https://isavdo.com/s/{unique_code}')
    )
    await bot.send_photo(message.chat.id, photo=photoUrl, caption=res['data']['telegram_description'],
                         reply_markup=inlineKeyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
