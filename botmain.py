import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from admin_handlers.admin import router as admin_router
from download_handlers.downloader import router as download_router
from databases.db_manager import add_user

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Register routers
dp.include_router(admin_router)
dp.include_router(download_router)

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Noma'lum"
    full_name = message.from_user.full_name
    
    # Add user to database
    await add_user(user_id, username, full_name or "Noma'lum")
    
    await message.reply(f"Salom {full_name}! Menga video yoki musiqa havolasini yuboring, men uni yuklab beraman.")

async def main():
    # Start polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
