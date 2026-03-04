import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, BaseMiddleware
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from admin_handlers.admin import router as admin_router
from download_handlers.downloader import router as download_router
from databases.db_manager import add_user, get_user, get_setting

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# --- Middleware for Blocking and Maintenance ---
class AccessMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: types.Message, data):
        user_id = event.from_user.id
        
        # Check maintenance mode
        maintenance = await get_setting("maintenance_mode")
        if maintenance == "true" and user_id != ADMIN_ID:
            await event.answer("🛠 Botda texnik ishlar olib borilmoqda. Iltimos, birozdan so'ng urinib ko'ring.")
            return

        # Check if user is blocked
        user = await get_user(user_id)
        if user and user.get("is_blocked") and user_id != ADMIN_ID:
            await event.answer("🚫 Siz botdan foydalanishdan chetlatilgansiz.")
            return
            
        return await handler(event, data)

# Register middleware
dp.message.middleware(AccessMiddleware())

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
    
    # Get custom welcome text
    welcome_text = await get_setting("welcome_text") or f"Salom {full_name}! Menga havola yuboring, men uni yuklab beraman."
    
    await message.reply(welcome_text)

async def main():
    # Start polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
