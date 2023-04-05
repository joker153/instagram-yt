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

# API endpoint and headers
url = "https://aiov-download-youtube-videos.p.rapidapi.com/GetVideoDetails"
headers = {
    "X-RapidAPI-Key": "6923523517msha40bbd50901ebdfp19ae30jsn37c67364b1c0",
    "X-RapidAPI-Host": "aiov-download-youtube-videos.p.rapidapi.com"
}

# Initialize the Pyrogram client
app = Client("my_bot_token", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


# Start message
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "Hello! I am a video downloader bot. Just send me a link to a YouTube, Instagram, Facebook, Snapchat, TikTok, Koo, or LinkedIn video, and I'll download it for you!"
    )


# Video downloader using API
@app.on_message(filters.regex("(?i)https?://(?:www\.)?(?:youtube\.com|youtu\.be|instagram\.com|facebook\.com|snapchat\.com|tiktok\.com|koo\.app|linkedin\.com)/.*"))
async def download_video(client, message):
    try:
        url = message.matches[0].group(0)
        querystring = {"URL": url}
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()

        # Check if the video is available for download
        if not data.get("DownloadInfo"):
            await message.reply_text("Sorry, the video is not available for download.")
            return

        # Get the download URL and file extension
        download_url = data["DownloadInfo"]["DownloadUrl"]
        extension = data["DownloadInfo"]["Ext"]

        # Download the video
        filename = f"{message.chat.id}.{extension}"
        response = requests.get(download_url, stream=True)
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)

        # Send the downloaded video to the chat
        caption = f"Title: {data['Title']}\nSize: {data['Size']}\nType: {data['Type']}"
        await client.send_video(
            chat_id=message.chat.id,
            video=filename,
            caption=caption,
            thumb=data["ThumbnailUrl"],
        )

    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

    finally:
        if os.path.exists(filename):
            os.remove(filename)


app.run()
