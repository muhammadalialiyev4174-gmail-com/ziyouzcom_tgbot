from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import db

categories = db.select_all_category()

index = 0
i = 0
keyboard = []
for category in categories:
    if i % 2 == 0 and i != 0:
        index += 1
    if i % 2 == 0:
        keyboard.append([KeyboardButton(text=category[1])])
    else:
        keyboard[index].append(KeyboardButton(text=category[1]))
    i += 1
keyboard.append([KeyboardButton(text="⬅️ Ortga")])
menu = ReplyKeyboardMarkup(keyboard=keyboard,resize_keyboard=True)

start_menu = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="📚 Ziyouz kutubxonasi"),
        ],
        [
            KeyboardButton(text="🗒 Qo`llanma"),
            KeyboardButton(text="KUTUBXONA RIVOJIGA HISSA")
        ],
    ],
    resize_keyboard = True,
)