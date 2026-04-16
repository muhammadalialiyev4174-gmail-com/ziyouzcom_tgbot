import pprint
import requests
import re
from bs4 import BeautifulSoup
import asyncio

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from loader import dp,db,bot
from keyboards.default.category import menu

# kutubxona bo`limlari uchun tugmalar yaratish
head_url= "https://n.ziyouz.com"
categories = db.select_all_category()

@dp.message_handler(text="📚 Ziyouz kutubxonasi")
async def kutubxona_handler(message: types.Message):
    await message.answer(f"Bosh sahifa", reply_markup=menu)

@dp.message_handler(text=[category[1] for category in categories])
async def category_handler(message: types.Message):
    category_books = db.select_any_category_books(typ=message.text)
    
    index = 0
    i = 0
    keyboard = []
    for subcategory in category_books:
        if i % 2 == 0 and i != 0:
            index += 1
        if i % 2 == 0:
            keyboard.append([KeyboardButton(text=subcategory[1])])
        else:
            keyboard[index].append(KeyboardButton(text=subcategory[1]))
        i += 1
    keyboard.append([KeyboardButton(text="◀️ Ortga")])
    category_list = ReplyKeyboardMarkup(keyboard=keyboard,resize_keyboard=True)
    
    await message.reply(f"Bo`limlar",reply_markup=category_list)
    
# ortga tugmasi
@dp.message_handler(text="◀️ Ortga")
async def back_handler(message: types.Message):
    await message.answer(text="📜 Bosh sahifa",reply_markup = menu)

# inline kitoblar ro`yxatini yaratish
category_books = db.select_all_category_books()
@dp.message_handler(text=[category_book[1] for category_book in category_books])
async def books_handler(message: types.Message):
    category_book = db.select_category_books(name=message.text)
    url = head_url+category_book[3]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    subcategories = soup.find_all("div", class_="pd-float")
    
    i = 0
    inline_keyboard = []
    row = []
    inline_number = 1
    reply_text = ""
    if len(subcategories)<=15:
        for subcategory in subcategories:
            reply_text += str(inline_number)+'. '+ subcategory.text + "\n"
            link = subcategory.find("a")["href"] 
            def get_number(url):
                match = re.search(r"download=(\d+)", url)
                if match:
                    return match.group(1)
                else:
                    return None
            number = get_number(link)
            data = f"{category_book[0]} {number}"
            row.append(InlineKeyboardButton(text=inline_number,callback_data=data))
            print(inline_number)
            if i % 4 == 0 and i != 0:
                inline_keyboard.append(row)
                row = []
            i += 1
            inline_number += 1
        if row:
            inline_keyboard.append(row)
    else:
        for subcategory in subcategories[:15]:
            reply_text +=str(inline_number)+'. '+ subcategory.text + "\n"
            link = subcategory.find("a")["href"] 
            def get_number(url):
                match = re.search(r"download=(\d+)", url)
                if match:
                    return match.group(1)
                else:
                    return None
            number = get_number(link)
            data = f"{category_book[0]} {number}"
            row.append(InlineKeyboardButton(text=inline_number,callback_data=data))
            print(inline_number)
            if i % 4 == 0 and i != 0:
                inline_keyboard.append(row)
                pprint.pprint(str(inline_number))
                row = []
            i += 1
            inline_number += 1
        if row:
            inline_keyboard.append(row)

        inline_keyboard.append([InlineKeyboardButton(text="Davomi ➡️",callback_data=f"next {category_book[0]}")])
    inline_buttons = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    empty_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Ortga")]],resize_keyboard=True)
    await message.reply(text=reply_text,reply_markup=inline_buttons)
    await bot.send_message(chat_id=message.chat.id, text="Kitoblar ⬆️", reply_markup=empty_keyboard)

# callback so`rovlar uchun handler
@dp.callback_query_handler()
async def callback_handler(callback: types.CallbackQuery):
    if callback.data.startswith("next"):
        book_id = callback.data.split(' ')[1]
        category_book = db.select_category_books(id=book_id)
        url = head_url+category_book[3]
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
    
        subcategories = soup.find_all("div", class_="pd-float")
    
        i = 0
        inline_keyboard = []
        inline_number = 16
        reply_text = ""
        row = []
        if len(subcategories)<30:
            for subcategory in subcategories[15:]:
                reply_text += str(inline_number)+'. '+ subcategory.text + "\n"
                link = subcategory.find("a")["href"] 
                def get_number(url):
                    match = re.search(r"download=(\d+)", url)
                    if match:
                        return match.group(1)
                    else:
                        return None
                number = get_number(link)
                data = f"{category_book[0]} {number}"
                row.append(InlineKeyboardButton(text=inline_number,callback_data=data))
                if i % 4 == 0 and i != 0:
                    inline_keyboard.append(row)
                    row = []
                i += 1
                inline_number += 1
            if row:
                inline_keyboard.append(row)
            inline_keyboard.append([InlineKeyboardButton(text="⬅️ Avvalgi",callback_data=f"before {category_book[0]}")])

        else:
            for subcategory in subcategories[15:30]:
                reply_text += str(inline_number)+'. '+ subcategory.text + "\n"
                link = subcategory.find("a")["href"] 
                def get_number(url):
                    match = re.search(r"download=(\d+)", url)
                    if match:
                        return match.group(1)
                    else:
                        return None
                number = get_number(link)
                data = f"{category_book[0]} {number}"
                row.append(InlineKeyboardButton(text=inline_number,callback_data=data))
                if i % 4 == 0 and i != 0:
                    inline_keyboard.append(row)
                    row = []
                i += 1
                inline_number += 1
            if row:
                inline_keyboard.append(row)
            inline_keyboard.append([InlineKeyboardButton(text="⬅️ Avvalgi",callback_data=f"before {category_book[0]}")])
        inline_buttons = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=reply_text,
        )
        await bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=inline_buttons,
        )
        
    elif callback.data.startswith("before"):
        book_id = callback.data.split(' ')[1]
        category_book = db.select_category_books(id=book_id)
        url = head_url+category_book[3]
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
    
        subcategories = soup.find_all("div", class_="pd-float")
    
        i = 0
        inline_keyboard = []
        inline_number = 1
        reply_text = ""
        row = []
        for subcategory in subcategories[:15]:
            reply_text += str(inline_number)+'. '+ subcategory.text + "\n"
            link = subcategory.find("a")["href"] 
            def get_number(url):
                match = re.search(r"download=(\d+)", url)
                if match:
                    return match.group(1)
                else:
                    return None
            number = get_number(link)
            data = f"{category_book[0]} {number}"
            row.append(InlineKeyboardButton(text=inline_number,callback_data=data))
            if i % 4 == 0 and i != 0:
                inline_keyboard.append(row)
                print(row,inline_number)
                row = []
            i += 1
            inline_number += 1
        if row:
            inline_keyboard.append(row)
        inline_keyboard.append([InlineKeyboardButton(text="Davomi ➡️",callback_data=f"next {category_book[0]}")])
        inline_buttons = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=reply_text,
        )
        await bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=inline_buttons,
        )
        
    else:    
        await callback.answer("So`rov jo`natildi.")
        sent_msg = await callback.message.answer("Kitob yuborilmoqda...")

        # callback_data matni
        data = callback.data
        data = data.split(' ')
        category_book = db.select_category_books(id=data[0])
        url = head_url+category_book[3]
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        subcategories = soup.find_all("div", class_="pd-float")
        for subcategory in subcategories:
            link = subcategory.find("a")["href"] 
            book_id = f"download={data[1]}"
            if re.search(book_id,link):
                get_link = head_url+link
                name = subcategory.text
                text = f"{name}\n<b>Manba</b>: ziyouz.com"
                break
            else:
                continue
        print(get_link)
        # Reply to callback query
        try:
            print("X")
            await bot.send_document(chat_id=callback.from_user.id, document=get_link, caption=text)
            await bot.delete_message(callback.message.chat.id, sent_msg.message_id)
        except Exception as e:
            await bot.delete_message(callback.message.chat.id, sent_msg.message_id)
            print("XXX")
            url = get_link
            site_link = InlineKeyboardMarkup(inline_keyboard = [
                [
                    InlineKeyboardButton(text="Saytga o`tish", url = url),
                ]
            ])
            text = f"⚙️ <b>Texnik sabablar tufayli \"{name}\" faylini Telegramga jo`natib bo`lmadi.</b>\n\n🔗 Quyidagi havola orqali Ziyouz saytining rasmiy sahifasida ushbu kitobdan foydalanishingiz mumkin.👇👇👇"
            await bot.send_message(chat_id=callback.from_user.id, text=text, reply_markup=site_link)