from flask import Flask
import asyncio
import os
import logging
from telethon import TelegramClient
from config import API_ID, API_HASH, PHONE, GROUP_ID

# Logging setup for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create downloads folder if not exists
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Initialize Flask App
app = Flask(__name__)

# Initialize Telegram Client
client = TelegramClient("session_name", API_ID, API_HASH)

async def download_pdfs():
    await client.start(PHONE)
    logger.info("✅ Logged in successfully!")

    async for message in client.iter_messages(GROUP_ID, limit=10):  # Adjust limit if needed
        if message.media and message.document and message.document.mime_type == "application/pdf":
            file_name = message.document.attributes[0].file_name or "unknown.pdf"
            file_path = os.path.join(DOWNLOAD_FOLDER, file_name)

            logger.info(f"Downloading: {file_name}")
            await client.download_media(message, file=file_path)
            logger.info(f"✅ Downloaded: {file_name}")

    await client.disconnect()

@app.route("/")
def home():
    return "Telegram PDF Downloader is Running!"

@app.route("/start-download")
def start_download():
    asyncio.create_task(download_pdfs())
    return "Downloading PDFs in the background!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
