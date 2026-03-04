import os
import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from databases.db_manager import get_users_count, get_all_users, block_user, get_downloads_count, update_setting, get_setting
from xkeyboards.keyboards import get_admin_keyboard, get_settings_keyboard, get_cancel_keyboard
from dotenv import load_dotenv

load_dotenv()
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

router = Router()

class AdminStates(StatesGroup):
    waiting_for_broadcast = State()
    waiting_for_block_id = State()
    waiting_for_welcome_text = State()

# --- Admin Panel Main ---
@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("🛠 **Admin Panelga xush kelibsiz!**", reply_markup=get_admin_keyboard())
    else:
        await message.answer("❌ Siz admin emassiz.")

@router.message(F.text == "🏠 Bosh menyu")
async def back_to_main(message: Message):
    await message.answer("🏠 Bosh menyu", reply_markup=get_admin_keyboard())

# --- Statistics ---
@router.message(F.text == "📊 Statistika")
async def show_stats(message: Message):
    if message.from_user.id == ADMIN_ID:
        u_count = await get_users_count()
        d_count = await get_downloads_count()
        await message.answer(f"📊 **Bot Statistikasi:**\n\n👤 Foydalanuvchilar: {u_count}\n📥 Jami yuklashlar: {d_count}")

# --- Broadcast (Reklama) ---
@router.message(F.text == "📢 Reklama")
async def start_broadcast(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        await message.answer("📢 Reklama xabarini yuboring (Matn, Rasm, Video bo'lishi mumkin):", reply_markup=get_cancel_keyboard())
        await state.set_state(AdminStates.waiting_for_broadcast)

@router.message(AdminStates.waiting_for_broadcast)
async def process_broadcast(message: Message, state: FSMContext, bot: Bot):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi.", reply_markup=get_admin_keyboard())
        return

    users = await get_all_users()
    count = 0
    await message.answer(f"⏳ Reklama {len(users)} ta foydalanuvchiga yuborilmoqda...")
    
    for user in users:
        try:
            await bot.copy_message(chat_id=user['id'], from_chat_id=message.chat.id, message_id=message.message_id)
            count += 1
            await asyncio.sleep(0.05) # Rate limit protection
        except Exception:
            pass
            
    await message.answer(f"✅ Reklama {count} ta foydalanuvchiga muvaffaqiyatli yuborildi!", reply_markup=get_admin_keyboard())
    await state.clear()

# --- Block User ---
@router.message(F.text == "🚫 Bloklash")
async def start_block(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        await message.answer("🚫 Bloklanadigan foydalanuvchi ID sini yuboring:", reply_markup=get_cancel_keyboard())
        await state.set_state(AdminStates.waiting_for_block_id)

@router.message(AdminStates.waiting_for_block_id)
async def process_block(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi.", reply_markup=get_admin_keyboard())
        return

    try:
        user_id = int(message.text)
        await block_user(user_id, True)
        await message.answer(f"✅ Foydalanuvchi {user_id} bloklandi.", reply_markup=get_admin_keyboard())
    except ValueError:
        await message.answer("❌ Noto'g'ri ID. Faqat raqam yuboring.")
    except Exception as e:
        await message.answer(f"❌ Xatolik: {str(e)}")
    finally:
        await state.clear()

# --- Settings ---
@router.message(F.text == "⚙️ Sozlamalar")
async def show_settings(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("⚙️ **Bot Sozlamalari:**", reply_markup=get_settings_keyboard())

@router.callback_query(F.data == "toggle_maintenance")
async def toggle_maintenance(callback: CallbackQuery):
    current = await get_setting("maintenance_mode")
    new_val = "true" if current == "false" else "false"
    await update_setting("maintenance_mode", new_val)
    await callback.answer(f"🛠 Texnik ishlar: {new_val.upper()}")

@router.callback_query(F.data == "edit_welcome")
async def edit_welcome(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("📝 Yangi start matnini yuboring:", reply_markup=get_cancel_keyboard())
    await state.set_state(AdminStates.waiting_for_welcome_text)
    await callback.answer()

@router.message(AdminStates.waiting_for_welcome_text)
async def process_welcome_text(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi.", reply_markup=get_admin_keyboard())
        return

    await update_setting("welcome_text", message.text)
    await message.answer("✅ Start matni yangilandi!", reply_markup=get_admin_keyboard())
    await state.clear()
