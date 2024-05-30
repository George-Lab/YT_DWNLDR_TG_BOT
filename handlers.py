from aiogram import types, F, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
import logging
import yt_dlp
import os


router = Router()


# Download video using yt-dlp
def download_video(url):
    ydl_opts = {
        "outtmpl": "downloaded_video.%(ext)s",
        "format": "best",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


# Command handler to start the bot
@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Hi!\nSend me a video link, and I'll download it for you!")


# Message handler to process video links
@router.message()
async def message_handler(message: Message):
    url = message.text
    try:
        await message.reply("Downloading the video, please wait...")
        download_video(url)
        video_file = "downloaded_video.mp4"
        video_from_fs = FSInputFile(video_file)
        result = await message.answer_video(video_from_fs, caption=video_file)
        os.remove(video_file)  # Clean up the downloaded file
    except Exception as e:
        logging.error(f"Error: {e}")
        await message.reply("Sorry, there was an error processing your request.")
