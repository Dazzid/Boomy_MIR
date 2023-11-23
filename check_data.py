import os
import asyncio
from mutagen.easyid3 import EasyID3
import aiohttp
import logging

logging.basicConfig(level=logging.INFO)

async def fetch_html_content(session, url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Referer': 'https://soundcloud.com/',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.text()
            else:
                logging.error(f"Error: Unable to fetch HTML content. Status code: {response.status}")
                return None
    except Exception as e:
        logging.error(f"Error during request: {e}")
        return None

async def check_boomy(file_path, session):
    audio = EasyID3(file_path)
    soundcloud_url = audio.get('website', [''])[0]

    logging.info(f'MP3 File: {file_path}')
    logging.info(f'SoundCloud URL: {soundcloud_url}')

    html_content = await fetch_html_content(session, soundcloud_url)
    await asyncio.sleep(1)  # Add a delay of 1 second between requests

    is_boomy = html_content and 'Boomy Corporation' in html_content
    
    artist = audio.get('artist', [''])[0]
    logging.info('Artist: %s', artist)

    if artist == 'Wobinn' and is_boomy:
        logging.info('Boomy Corporation found in the HTML')
        logging.info('-' * 30)
        return file_path
    else:
        logging.info('Boomy Corporation not found in the HTML or Artist is not Wobinn')
        logging.info('-' * 30)
        return None

async def process_mp3_files(folder_path):
    wobinn_boomy_files = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.mp3'):
                    file_path = os.path.join(root, file)
                    tasks.append(check_boomy(file_path, session))

        results = await asyncio.gather(*tasks)

        wobinn_boomy_files = [result for result in results if result is not None]

    return wobinn_boomy_files

async def main():
    folder_path = '/workspace/wobinn/'
    good_files = await process_mp3_files(folder_path)
    print(len(good_files))

# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())
