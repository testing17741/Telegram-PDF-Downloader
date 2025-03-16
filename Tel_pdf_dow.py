import asyncio
import os
import logging
from telethon import TelegramClient
from config import API_ID, API_HASH, PHONE, GROUP_ID

# Setup logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

client = TelegramClient("session_name", API_ID, API_HASH)

async def download_pdf(message):
    try:
        file_name = message.document.attributes[0].file_name
    except (AttributeError, IndexError):
        file_name = "unknown.pdf"
    file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
    logger.info(f"Starting download: {file_name}")
    try:
        # Set a timeout of 60 seconds for each download
        await asyncio.wait_for(client.download_media(message, file=file_path), timeout=60)
        logger.info(f"Downloaded: {file_name}")
    except asyncio.TimeoutError:
        logger.error(f"Timeout while downloading {file_name}. Skipping.")
    except Exception as e:
        logger.error(f"Error downloading {file_name}: {e}")

async def main():
    await client.start(PHONE)
    logger.info("✅ Logged in successfully!")
    
    tasks = []
    total_messages = 0
    total_pdfs = 0

    async for message in client.iter_messages(GROUP_ID, limit=None):
        total_messages += 1
        if message.media and message.document and message.document.mime_type == "application/pdf":
            total_pdfs += 1
            tasks.append(download_pdf(message))
            
            # Process in batches of 5 to reduce load
            if len(tasks) >= 5:
                await asyncio.gather(*tasks)
                tasks = []
                logger.info(f"Processed {total_messages} messages; PDFs downloaded: {total_pdfs}")
                # Small delay between batches
                await asyncio.sleep(1)

    if tasks:
        await asyncio.gather(*tasks)
    
    logger.info(f"🎉 Completed! Total messages processed: {total_messages}, Total PDFs downloaded: {total_pdfs}")
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
