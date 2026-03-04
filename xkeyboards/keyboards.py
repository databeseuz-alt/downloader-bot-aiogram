from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="📢 Reklama")],
            [KeyboardButton(text="👥 Foydalanuvchilar"), KeyboardButton(text="🚫 Bloklash")],
            [KeyboardButton(text="⚙️ Sozlamalar"), KeyboardButton(text="🏠 Bosh menyu")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_settings_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛠 Texnik ishlar (On/Off)", callback_data="toggle_maintenance")],
        [InlineKeyboardButton(text="📝 Start matnini o'zgartirish", callback_data="edit_welcome")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin_back")]
    ])
    return keyboard

def get_download_options(url: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎬 Video", callback_data=f"dl_video_{url}"),
            InlineKeyboardButton(text="🎵 Audio (MP3)", callback_data=f"dl_audio_{url}")
        ],
        [
            InlineKeyboardButton(text="🖼 Rasm (Agar mavjud bo'lsa)", callback_data=f"dl_image_{url}")
        ]
    ])
    return keyboard

def get_cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
        resize_keyboard=True
    )
    return keyboard
