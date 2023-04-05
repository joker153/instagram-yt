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



@app.on_message(pyrogram.filters.command(["start"]))
def start(client, message):
    message.reply_text("Hi, send me a YouTube or Instagram video link to download the video.")

@app.on_message(pyrogram.filters.text)
def download_video(client, message):
    url = message.text
    valid_platforms = ["youtube.com", "www.youtube.com", "m.youtube.com", "youtube.com.br", "www.youtube.com.br", "instagram.com", "www.instagram.com"]
    if any(platform in url for platform in valid_platforms):
        try:
            video_details_url = "https://aiov-download-youtube-videos.p.rapidapi.com/GetVideoDetails"
            headers = {
                "X-RapidAPI-Key": "6923523517msha40bbd50901ebdfp19ae30jsn37c67364b1c0",
                "X-RapidAPI-Host": "aiov-download-youtube-videos.p.rapidapi.com"
            }
            params = {"URL": url}
            response = requests.get(video_details_url, headers=headers, params=params)
            data = response.json()

            video_url = data["StreamingURL"]
            title = data["VideoTitle"]
            file_type = data["FileType"]
            thumb_url = data["ThumbnailURL"]
            size = data["FileSize"]
            filename = f"{title}.{file_type}"
            if os.path.exists(filename):
                message.reply_text("Video already exists.")
            else:
                message.reply_text(f"Downloading {title}...")
                response = requests.get(video_url)
                with open(filename, "wb") as f:
                    f.write(response.content)
                message.reply_video(video=filename, caption=title)
                os.remove(filename)
        except Exception as e:
            message.reply_text(f"An error occurred: {str(e)}")
    else:
        message.reply_text("Invalid URL. Please send a valid YouTube or Instagram video link.")

app.run()
