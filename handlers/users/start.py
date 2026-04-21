import logging
from aiogram import types
from aiogram.filters import CommandStart
from keyboards.default.category import start_menu
from data.config import ADMINS
from loader import dp, db, bot

@dp.message(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    try:
        await db.add_user(id=message.from_user.id, name=name)
    except Exception as err:
        for admin in ADMINS:
            try:
                await bot.send_message(chat_id=admin, text=str(err))
            except:
                pass
   
    await message.reply(f"Assalomu alaykum, {name}! \nKutubxonamizga xush kelibsiz!\n", reply_markup=start_menu)
    
    try:
        count = await db.count_users()
        if count:
            msg = f"{name} bazaga qo'shildi.\nBazada {count[0]} ta foydalanuvchi bor."
            await bot.send_message(chat_id=ADMINS[0], text=msg)
    except Exception as e:
        logging.error(e)
