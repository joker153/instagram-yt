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

# Define the command to download Instagram videos
@app.on_message(filters.command("insta"))
async def insta(bot: Client, message: Message):
    # Get the Instagram post URL from the message
    url = message.text.split(" ")[1]

    # Download the post using Instaloader
    L = Instaloader()
    post = Post.from_shortcode(L.context, url)
    L.download_post(post, target="insta_videos")

    # Send the video file to the user
    video_file = f"insta_videos/{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
    await bot.send_video(chat_id=message.chat.id, video=video_file)

# Define the command to download YouTube videos
@app.on_message(filters.command("youtube"))
async def youtube(bot: Client, message: Message):
    # Get the YouTube video URL from the message
    url = message.text.split(" ")[1]

    # Download the video using Pytube
    video = YouTube(url)
    stream = video.streams.get_highest_resolution()
    stream.download(output_path="youtube_videos")

    # Send the video file to the user
    video_file = f"youtube_videos/{video.title}.mp4"
    await bot.send_video(chat_id=message.chat.id, video=video_file)

# Run the bot
if __name__ == "__main__":
    app.run()
