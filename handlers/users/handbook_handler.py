from aiogram import types
from loader import dp,db,bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.default.category import start_menu

@dp.message_handler(text="🗒 Qo`llanma")
async def kutubxona_handler(message: types.Message):
    text = """
    <b>Assalomu alaykum</b>, men ziyouz.com saytidagi kitoblarni telegramga jo`natib beruvchi botman. Botdan foydalanish uchun quyidagi qo`llanmani o`qing:

- Bot sizga kitob bo`limlarini tanlash uchun tanlov tugmalarini ko`rsatadi. Kerakli bo`limni tanlang.

- Sizga tanlangan bo`limdagi kitoblar ro`yxati ko`rsatiladi. O`zingizga kerakli kitobni tanlang.

- Bot sizga tanlangan kitobni Telegram orqali jo`natadi. Kitobni yuklab olish uchun, uning ustiga bosing.

❗️❗️❗️Botdan foydalanishda quyidagilarga e`tibor bering:

- Ba'zi kitoblarni texnik muammo tufayli Telegramga jo`natib bo`lmasligi mumkin. Bu holatda, bot sizga xatolik haqida xabar beradi va kitobni ziyouz.com saytidan yuklab olish uchun havola taqdim etadi.

‼️ Ziyo istagan qalblar uchun! Saytda taqdim etilgan elektron manbalardan faqatgina shaxsiy mutolaa maqsadida foydalanish mumkin. Tijoriy maqsadlarda foydalanish (sotish, chop etish, ko‘paytirish, tarqatish) qonunan taqiqlanadi. Saytdan materiallar olib chop etilganda manzilimiz koʻrsatilishi shart.
    """
    await message.answer(f"{text}", reply_markup=ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="⬅️ Ortga")]],resize_keyboard=True))

@dp.message_handler(text="KUTUBXONA RIVOJIGA HISSA")
async def send_photo(message: types.Message):
    photo = types.InputFile('data/paypal-uzcard.png')
    text = """Saytimiz rivojiga hissa qo‘shmoqchi bo‘lsangiz:

Uzcard plastik karta raqamimiz: <code>8600 5504 8563 9786</code>

Payoneer: davronbek@gmail.com"""
    await bot.send_photo(
        chat_id=message.chat.id, 
        photo=photo,
        caption=text
    )

@dp.message_handler(text="⬅️ Ortga")
async def kutubxona_handler(message: types.Message):
    name = message.from_user.full_name
    await message.reply(f"Assalomu alaykum, {name}! \n Xush kelibsiz!",reply_markup = start_menu)