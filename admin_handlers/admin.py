import os
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from databases.db_manager import get_users_count, get_all_users
from xkeyboards.keyboards import get_admin_keyboard
from dotenv import load_dotenv

load_dotenv()
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Xush kelibsiz, Admin!", reply_markup=get_admin_keyboard())
    else:
        await message.answer("Siz admin emassiz.")

@router.message(F.text == "📊 Statistika")
async def show_stats(message: Message):
    if message.from_user.id == ADMIN_ID:
        count = await get_users_count()
        await message.answer(f"📊 Bot foydalanuvchilari soni: {count}")

@router.message(F.text == "📢 Reklama")
async def broadcast_message(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Reklama yuborish uchun xabarni yozing (Hozircha faqat matnli xabarlar).")
        # Bu yerda FSM (Finite State Machine) orqali reklama yuborishni davom ettirish mumkin.

@router.message(F.text == "👥 Foydalanuvchilar")
async def list_users(message: Message):
    if message.from_user.id == ADMIN_ID:
        users = await get_all_users()
        user_list = "\n".join([f"{u['id']} - @{u['username']}" for u in users[:20]])
        await message.answer(f"Oxirgi 20 foydalanuvchi:\n{user_list}")
