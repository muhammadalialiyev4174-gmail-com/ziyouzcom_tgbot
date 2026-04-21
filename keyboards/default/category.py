from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

async def get_category_menu(db):
    categories = await db.select_all_category()
    builder = ReplyKeyboardBuilder()
    
    for category in categories:
        builder.button(text=category[1])
    
    builder.adjust(2)
    builder.row(KeyboardButton(text="⬅️ Ortga"))
    
    return builder.as_markup(resize_keyboard=True)

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📚 Ziyouz kutubxonasi"),
        ],
        [
            KeyboardButton(text="🗒 Qo`llanma"),
            KeyboardButton(text="KUTUBXONA RIVOJIGA HISSA")
        ],
    ],
    resize_keyboard=True,
)