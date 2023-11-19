import asyncio
import logging
import sys
import os

import httpx
from aiogram.types import BufferedInputFile, Message, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold
import aiogram.utils.markdown as md

from button import commands
from db.connection import create_user
from parser.instagram import download_insta
from parser.sptik import download_tik
from parser.story import profile, stories_list
from aiogram import types

from parser.yt import youtube_download

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    username = message.from_user.username or f"{message.from_user.first_name} {message.from_user.last_name}"
    create_user(username, message.from_user.id)
    await bot.set_my_commands(commands)
    await message.answer(f"Assalomu aleykum, {hbold(message.from_user.full_name)}")


@dp.message(lambda message: message.text.startswith('https://www.instagram.com/'))
async def insta_handler(message: Message):
    message_to_edit = await message.answer("🔎")
    url = message.text
    try:
        video = httpx.get(download_insta(url)).content
        if video != 'Error: Video is private. Please use the tool Instagram Private Downloader.':
            await message_to_edit.delete()
            await message.reply_video(video=BufferedInputFile(file=video, filename="test.mp4"),
                                      caption=md.text("@oson_yuklash_bot 𝕪𝕠𝕣𝕕𝕒𝕞𝕚𝕕𝕒 𝕪𝕦𝕜𝕝𝕒𝕟𝕕𝕚 📥"))
        else:
            await message_to_edit.delete()
            await message.answer("𝐩𝐫𝐢𝐯𝐚𝐭𝐞 𝐚𝐜𝐜𝐨𝐮𝐧𝐭 ⚠️ ")
    except httpx.ReadTimeout:
        print('Video hajmi juda katta')


@dp.message(lambda message: message.text.startswith('@'))
async def insta_handler(message: types.Message):
    message_to_edit = await message.answer("🔎")
    username = message.text[1:]
    if (profile_data := profile(username)) != '{TypeError}the JSON object must be str, bytes or bytearray, not int':
        inline_btn = InlineKeyboardButton(text='Download Stories', callback_data=f"inline_btn__{username}")
        inline_markup = InlineKeyboardMarkup(inline_keyboard=[[inline_btn]])
        if isinstance(profile_data, tuple):
            await message_to_edit.delete()
            image_url = profile_data[0]
            image_response = httpx.get(image_url)
            if image_response.status_code == 200:
                image_bytes = image_response.content
                caption = f"Followers: {profile_data[1]}\nFollowing: {profile_data[2]}\nFull Name: {profile_data[3]}\n"
                await message.answer_photo(photo=BufferedInputFile(file=image_bytes, filename='test.png'),
                                           caption=caption,
                                           reply_markup=inline_markup)
            else:
                await message.answer(f"Error downloading profile picture. Status code: {image_response.status_code}")
        else:
            await message_to_edit.delete()
            await message.answer(f"Error: {profile_data}")
    else:

        await message.answer(f"Akkaunt private yoki yaqinlar ko'rishi  uchun ochiq")




@dp.message(lambda message: message.text.startswith('https://www.tiktok.com/'))
async def tiktok(message: Message):
    await message.answer("🔎")
    url = message.text
    video = httpx.get(download_tik(url)).content
    try:
        await bot.send_video(chat_id=message.chat.id, video=BufferedInputFile(file=video, filename='test.mp4'),
                             caption=md.text("@oson_yuklash_bot 𝕪𝕠𝕣𝕕𝕒𝕞𝕚𝕕𝕒 𝕪𝕦𝕜𝕝𝕒𝕟𝕕𝕚 📥"))
    except ValueError:
        await message.answer(
            "𝘃𝗶𝗱𝗲𝗼 𝗹𝗶𝗺𝗶𝘁𝗱𝗮𝗻 𝗼𝘀𝗵𝗶𝗯 𝗸𝗲𝘁𝗴𝗮𝗻𝗹𝗶𝗴𝗶 𝘀𝗮𝗯𝗮𝗯𝗹𝗶 𝘆𝘂𝗸𝗹𝗮𝘀𝗵𝗻𝗶 𝗶𝗹𝗼𝗷𝗶 𝗯𝗼𝗹𝗺𝗮𝗱𝗶")


@dp.message(lambda message: message.text.startswith('https://youtu.be/'))
async def tiktok(message: Message):
    await message.answer("🔎")
    url = message.text
    video = httpx.get(youtube_download(url)).content
    try:
        await bot.send_video(chat_id=message.chat.id, video=BufferedInputFile(file=video, filename='test.mp4'),
                             caption=md.text("@oson_yuklash_bot 𝕪𝕠𝕣𝕕𝕒𝕞𝕚𝕕𝕒 𝕪𝕦𝕜𝕝𝕒𝕟𝕕𝕚 📥"))
    except ValueError:
        await message.answer(
            "𝘃𝗶𝗱𝗲𝗼 𝗹𝗶𝗺𝗶𝘁𝗱𝗮𝗻 𝗼𝘀𝗵𝗶𝗯 𝗸𝗲𝘁𝗴𝗮𝗻𝗹𝗶𝗴𝗶 𝘀𝗮𝗯𝗮𝗯𝗹𝗶 𝘆𝘂𝗸𝗹𝗮𝘀𝗵𝗻𝗶 𝗶𝗹𝗼𝗷𝗶 𝗯𝗼𝗹𝗺𝗮𝗱𝗶")


@dp.callback_query(lambda c: c.data.startswith('inline_btn__'))
async def process_inline_callback(callback_query: types.CallbackQuery):
    username = callback_query.data.split('__')[1]
    for i in stories_list(username):
        video = httpx.get(i).content
        await callback_query.message.answer_video(video=BufferedInputFile(file=video, filename='test.mp4'),
                                                  caption=md.text(
                                                      "@oson_yuklash_bot 𝕪𝕠𝕣𝕕𝕒𝕞𝕚𝕕𝕒 𝕪𝕦𝕜𝕝𝕒𝕟𝕕𝕚 📥"))


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
