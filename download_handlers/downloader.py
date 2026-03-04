import os
import yt_dlp
import asyncio
import re
from aiogram import Router, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from databases.db_manager import log_download
from xkeyboards.keyboards import get_download_options

router = Router()

COOKIES_PATH = "cookies.txt"

def get_ytdlp_opts(user_id: int, format_type: str = 'video'):
    if format_type == 'audio':
        opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'downloads/{user_id}_%(title)s.%(ext)s',
        }
    elif format_type == 'image':
        opts = {
            'format': 'best',
            'writethumbnail': True,
            'skip_download': True,
            'outtmpl': f'downloads/{user_id}_%(title)s.%(ext)s',
        }
    else: # video
        opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'downloads/{user_id}_%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
        }
    
    opts.update({
        'cookiefile': COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
        'max_filesize': 50 * 1024 * 1024, # 50MB limit
        'quiet': True,
        'no_warnings': True,
    })
    return opts

def download_media(url: str, user_id: int, format_type: str = 'video'):
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
        
    opts = get_ytdlp_opts(user_id, format_type)
    
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        
        if format_type == 'audio':
            filename = filename.rsplit('.', 1)[0] + '.mp3'
        elif format_type == 'image':
            filename = info.get('thumbnail')
            
        return filename, info.get('extractor_key', 'unknown')

@router.message(F.text.regexp(r'https?://[^\s]+'))
async def handle_url(message: Message):
    url = message.text
    await message.answer("📥 Media turini tanlang:", reply_markup=get_download_options(url))

@router.callback_query(F.data.startswith("dl_"))
async def process_download(callback: CallbackQuery):
    data = callback.data.split("_")
    format_type = data[1]
    url = "_".join(data[2:])
    
    await callback.message.edit_text(f"⏳ {format_type.capitalize()} yuklanmoqda...")
    
    try:
        loop = asyncio.get_event_loop()
        file_path, platform = await loop.run_in_executor(None, download_media, url, callback.from_user.id, format_type)
        
        if file_path and os.path.exists(file_path):
            media_file = FSInputFile(file_path)
            
            if format_type == 'video':
                await callback.message.answer_video(media_file, caption=f"✅ @{callback.bot.username} orqali yuklandi")
            elif format_type == 'audio':
                await callback.message.answer_audio(media_file, caption=f"✅ @{callback.bot.username} orqali yuklandi")
            elif format_type == 'image':
                await callback.message.answer_photo(media_file, caption=f"✅ @{callback.bot.username} orqali yuklandi")
            
            await log_download(callback.from_user.id, url, format_type, platform)
            
            # Clean up
            if os.path.exists(file_path):
                os.remove(file_path)
        else:
            await callback.message.answer("❌ Faylni yuklab bo'lmadi yoki hajmi juda katta (50MB+).")
            
    except Exception as e:
        await callback.message.answer(f"❌ Xatolik: {str(e)}")
    finally:
        await callback.message.delete()
        await callback.answer()
