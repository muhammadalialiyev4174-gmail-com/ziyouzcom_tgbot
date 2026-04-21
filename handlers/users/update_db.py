from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

from loader import dp, db

class EmailState(StatesGroup):
    email = State()

@dp.message(Command("email"))
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer("Email manzilingizni yuboring")
    await state.set_state(EmailState.email)

@dp.message(EmailState.email)
async def enter_email(message: types.Message, state: FSMContext):
    email = message.text
    await db.update_user_email(email=email, id=message.from_user.id)
    user = await db.select_user(id=message.from_user.id)
    await message.answer(f"Baza yangilandi: {user}")
    await state.clear()
