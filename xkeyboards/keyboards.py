from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="📢 Reklama")],
            [KeyboardButton(text="👥 Foydalanuvchilar"), KeyboardButton(text="⚙️ Sozlamalar")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_download_options(url: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎬 Video", callback_data=f"dl_video_{url}"),
            InlineKeyboardButton(text="🎵 Audio", callback_data=f"dl_audio_{url}")
        ]
    ])
    return keyboard
