import io
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold
from aiogram.methods.get_file import GetFile

import asyncio
import logging
import sys

from config import tg_token
from hotdog import predict

dp = Dispatcher()
bot = Bot(token=tg_token)


@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message()
async def show_weather(message: types.input_media_photo):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    raw = await bot.download_file(file_path)
    result = predict(raw)
    await message.reply(result)


async def main() -> None:
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
