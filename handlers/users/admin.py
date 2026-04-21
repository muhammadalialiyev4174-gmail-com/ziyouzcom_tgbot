import asyncio
from aiogram import types
from aiogram import F

from data.config import ADMINS
from loader import dp, db, bot

@dp.message(F.text == "/allusers", F.from_user.id.in_(list(map(int, ADMINS))))
async def get_all_users(message: types.Message):
    users = await db.select_all_users()
    await message.answer(str(users))

@dp.message(F.text == "/reklama", F.from_user.id.in_(list(map(int, ADMINS))))
async def send_ad_to_all(message: types.Message):
    users = await db.select_all_users()
    for user in users:
        user_id = user[0]
        try:
            await bot.send_message(chat_id=user_id, text="@SariqDev kanaliga obuna bo'ling!")
        except Exception:
            pass
        await asyncio.sleep(0.05)

@dp.message(F.text == "/cleandb", F.from_user.id.in_(list(map(int, ADMINS))))
async def clean_all_users(message: types.Message):
    await db.delete_users()
    await message.answer("Baza tozalandi!")