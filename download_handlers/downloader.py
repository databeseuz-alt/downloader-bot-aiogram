import os
import yt_dlp
import asyncio
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from databases.db_manager import log_download

router = Router()

COOKIES_PATH = "cookies.txt"

def download_video(url: str, user_id: int):
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'downloads/{user_id}_%(title)s.%(ext)s',
        'cookiefile': COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
        'max_filesize': 50 * 1024 * 1024, # 50MB limit for Telegram
    }
    
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename

@router.message(F.text.startswith("http"))
async def handle_url(message: Message):
    url = message.text
    status_msg = await message.answer("⏳ Yuklanmoqda...")
    
    try:
        # Run blocking download in a separate thread
        loop = asyncio.get_event_loop()
        file_path = await loop.run_in_executor(None, download_video, url, message.from_user.id)
        
        if os.path.exists(file_path):
            video = FSInputFile(file_path)
            await message.answer_video(video, caption="✅ Yuklab olindi!")
            await log_download(message.from_user.id, url, "video")
            os.remove(file_path)
        else:
            await message.answer("❌ Faylni yuklab bo'lmadi.")
            
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")
    finally:
        await status_msg.delete()
