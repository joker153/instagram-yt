import os
import re
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

# Set up the Telegram API client
api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')
app = Client('video_downloader_bot', api_id, api_hash, bot_token=bot_token)

# Define the commands that the bot will recognize
commands = ['/start', '/help']

# Define the download function
def download_video(url):
    # Check if the URL is from Instagram or YouTube
    if 'instagram.com' in url:
        # Download the Instagram video
        page = requests.get(url).text
        video_url = re.search('property="og:video" content="(.*?)"', page).group(1)
        filename = 'instagram.mp4'
    elif 'youtube.com' in url:
        # Download the YouTube video
        video_url = f'https://www.youtube.com/watch?v={url.split("?v=")[-1]}'
        # Get the highest quality available
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(video_url, headers=headers)
        formats = re.findall('"adaptiveFormats":(.*?),"adaptiveFormats"', response.text)
        format = max(formats, key=lambda x: int(re.search('"qualityLabel":"(\d+)p"', x).group(1)))
        video_url = re.search('"url":"(.*?)"', format).group(1)
        filename = 'youtube.mp4'
    else:
        return None

    # Download the video
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(video_url, headers=headers, stream=True)
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return filename

# Define the start command handler
@app.on_message(filters.command('start'))
def start_handler(client: Client, message: Message):
    message.reply_text('Welcome to the video downloader bot! To download a video, send me a message with the URL.')

# Define the help command handler
@app.on_message(filters.command('help'))
def help_handler(client: Client, message: Message):
    message.reply_text('To download a video, send me a message with the URL.')

# Define the message handler
@app.on_message(filters.text)
def message_handler(client: Client, message: Message):
    # Parse the message text
    url = message.text.strip()

    # Download the video
    filename = download_video(url)
    if filename is None:
        message.reply_text('Invalid URL. Please send a valid Instagram or YouTube URL.')
        return

    # Send the video to the user
    message.reply_video(filename, supports_streaming=True)

    # Delete the downloaded file
    os
