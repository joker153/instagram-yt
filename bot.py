import os
import pyrogram
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from pytube import YouTube
from instaloader import Instaloader, Post

# Get the API ID, API Hash, and bot token from environment variables
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")

# Initialize the Pyrogram client
app = Client("my_bot_token", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


@app.on_message(filters.regex("(?i)https?://(?:www\.)?(?:instagram\.com|instagr\.am)/p/.*"))
async def insta(client, message):
    try:
        url = message.matches[0].group(0)
        insta = instaloader.Instaloader()
        insta.download_video(url, target=f"{message.chat.id}.mp4")
        await client.send_video(
            chat_id=message.chat.id,
            video=f"{message.chat.id}.mp4",
            caption="Here is the requested video!",
        )
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
    finally:
        if os.path.exists(f"{message.chat.id}.mp4"):
            os.remove(f"{message.chat.id}.mp4")


@app.on_message(filters.regex("(?i)https?://(?:www\.)?(?:youtube\.com|youtu\.be)/.*"))
async def youtube(client, message):
    try:
        url = message.matches[0].group(0)
        yt = pytube.YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=".", filename=f"{message.chat.id}.mp4")
        await client.send_video(
            chat_id=message.chat.id,
            video=f"{message.chat.id}.mp4",
            caption="Here is the requested video!",
        )
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
    finally:
        if os.path.exists(f"{message.chat.id}.mp4"):
            os.remove(f"{message.chat.id}.mp4")


app.run()
