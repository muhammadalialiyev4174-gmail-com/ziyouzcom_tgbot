import logging
import re
import asyncio
import os
import aiohttp
from bs4 import BeautifulSoup
from cachetools import TTLCache

from aiogram import types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from loader import dp, db, bot
from keyboards.default.category import get_category_menu, start_menu

head_url = "https://n.ziyouz.com"

# Cache for 10 minutes to avoid hitting Ziyouz for every page turn
# Key: url, Value: list of dictionaries {"text": str, "url": str, "number": str}
subcategories_cache = TTLCache(maxsize=100, ttl=600)

async def fetch_and_parse_books(url: str):
    if url in subcategories_cache:
        return subcategories_cache[url]
        
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=15) as response:
                if response.status != 200:
                    logging.error(f"Failed to fetch {url}, status code {response.status}")
                    return []
                html = await response.text()
        except Exception as e:
            logging.error(f"Error fetching {url}: {e}")
            return []

    soup = BeautifulSoup(html, "html.parser")
    subcategories = soup.find_all("div", class_="pd-float")
    
    parsed_data = []
    for subcategory in subcategories:
        link = subcategory.find("a")
        if not link:
            continue
        href = link["href"]
        match = re.search(r"download=(\d+)", href)
        if match:
            number = match.group(1)
            parsed_data.append({
                "text": subcategory.text.strip(),
                "url": head_url + href,
                "number": number
            })
    
    subcategories_cache[url] = parsed_data
    return parsed_data

def generate_books_keyboard(parsed_data, category_id, page=1, items_per_page=15):
    builder = InlineKeyboardBuilder()
    
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    current_page_items = parsed_data[start_idx:end_idx]
    
    reply_text = ""
    inline_number = start_idx + 1
    
    for item in current_page_items:
        reply_text += f"{inline_number}. {item['text']}\n"
        data = f"book_{category_id}_{item['number']}"
        builder.button(text=str(inline_number), callback_data=data)
        inline_number += 1
        
    builder.adjust(4)
    
    # Pagination buttons
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Avvalgi", callback_data=f"page_{category_id}_{page-1}"))
    if end_idx < len(parsed_data):
        nav_buttons.append(InlineKeyboardButton(text="Davomi ➡️", callback_data=f"page_{category_id}_{page+1}"))
        
    if nav_buttons:
        builder.row(*nav_buttons)
        
    return reply_text, builder.as_markup()


@dp.message(F.text == "📚 Ziyouz kutubxonasi")
async def kutubxona_handler(message: types.Message):
    menu = await get_category_menu(db)
    await message.answer("Bosh sahifa", reply_markup=menu)


@dp.message(lambda msg: msg.text and msg.text != "⬅️ Ortga" and msg.text != "📚 Ziyouz kutubxonasi" and msg.text != "🗒 Qo`llanma" and msg.text != "KUTUBXONA RIVOJIGA HISSA" and not msg.text.startswith("/"))
async def dynamic_category_handler(message: types.Message):
    # Determine if text is a category or a subcategory
    # First, let's check if it's a category
    categories = await db.select_all_category()
    category_names = [cat[1] for cat in categories]
    
    if message.text in category_names:
        category_books = await db.select_any_category_books(typ=message.text)
        builder = ReplyKeyboardBuilder()
        for subcategory in category_books:
            builder.button(text=subcategory[1])
        builder.adjust(2)
        builder.row(KeyboardButton(text="◀️ Ortga"))
        await message.reply("Bo`limlar", reply_markup=builder.as_markup(resize_keyboard=True))
        return

    # If it's a subcategory (book category)
    category_book = await db.select_category_books(name=message.text)
    if not category_book:
        return
        
    url = head_url + category_book[3]
    parsed_data = await fetch_and_parse_books(url)
    
    if not parsed_data:
        await message.reply("Kechirasiz, ushbu bo'limdan ma'lumot topilmadi yoki sayt vaqtinchalik ishlamayapti.")
        return
        
    reply_text, inline_markup = generate_books_keyboard(parsed_data, category_book[0], page=1)
    
    empty_keyboard = ReplyKeyboardBuilder()
    empty_keyboard.button(text="◀️ Ortga")
    
    await message.reply(text=reply_text, reply_markup=inline_markup)
    await bot.send_message(chat_id=message.chat.id, text="Kitoblar ⬆️", reply_markup=empty_keyboard.as_markup(resize_keyboard=True))


@dp.message(F.text == "◀️ Ortga")
async def back_handler(message: types.Message):
    menu = await get_category_menu(db)
    await message.answer(text="📜 Bosh sahifa", reply_markup=menu)


@dp.callback_query(F.data.startswith("page_"))
async def pagination_handler(callback: types.CallbackQuery):
    _, category_id, page_str = callback.data.split("_")
    page = int(page_str)
    
    category_book = await db.select_category_books(id=category_id)
    if not category_book:
        await callback.answer("Xatolik yuz berdi.", show_alert=True)
        return
        
    url = head_url + category_book[3]
    parsed_data = await fetch_and_parse_books(url)
    
    if not parsed_data:
        await callback.answer("Ma'lumot topilmadi.", show_alert=True)
        return
        
    reply_text, inline_markup = generate_books_keyboard(parsed_data, category_id, page=page)
    
    await callback.message.edit_text(text=reply_text, reply_markup=inline_markup)
    await callback.answer()


@dp.callback_query(F.data.startswith("book_"))
async def book_download_handler(callback: types.CallbackQuery):
    _, category_id, book_number = callback.data.split("_")
    
    await callback.answer("So`rov jo`natildi. Kitob yuklanmoqda...")
    sent_msg = await callback.message.answer("Kitob yuklab olinmoqda, kuting...")
    
    category_book = await db.select_category_books(id=category_id)
    if not category_book:
        await bot.delete_message(callback.message.chat.id, sent_msg.message_id)
        return
        
    url = head_url + category_book[3]
    parsed_data = await fetch_and_parse_books(url)
    
    target_book = None
    for item in parsed_data:
        if item["number"] == book_number:
            target_book = item
            break
            
    if not target_book:
        await bot.delete_message(callback.message.chat.id, sent_msg.message_id)
        await callback.message.answer("Kitob topilmadi.")
        return
        
    book_url = target_book["url"]
    book_name = target_book["text"]
    
    caption_text = f"<b>{book_name}</b>\n\n<b>Manba</b>: ziyouz.com"
    
    # Download the file to /tmp/ async
    tmp_path = f"/tmp/{book_number}_{os.path.basename(book_url.split('?')[0])}"
    if not tmp_path.endswith('.pdf') and not tmp_path.endswith('.zip') and not tmp_path.endswith('.rar'):
        tmp_path += ".pdf" # Default fallback extension
        
    try:
        async with aiohttp.ClientSession() as session:
            # First check headers for file size
            async with session.head(book_url, allow_redirects=True) as head_resp:
                content_length = head_resp.headers.get("Content-Length")
                if content_length and int(content_length) > 49 * 1024 * 1024:
                    # File larger than 50MB
                    raise ValueError("File is larger than Telegram limit (50MB).")
            
            # Now download
            async with session.get(book_url, allow_redirects=True) as resp:
                if resp.status == 200:
                    with open(tmp_path, "wb") as f:
                        while True:
                            chunk = await resp.content.read(1024 * 1024)
                            if not chunk:
                                break
                            f.write(chunk)
                else:
                    raise Exception(f"Failed to download, status: {resp.status}")
        
        # Send to user
        file_to_send = FSInputFile(tmp_path)
        await bot.send_document(chat_id=callback.from_user.id, document=file_to_send, caption=caption_text)
        await bot.delete_message(callback.message.chat.id, sent_msg.message_id)
        
        # Cleanup
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
            
    except Exception as e:
        logging.error(f"Download error: {e}")
        await bot.delete_message(callback.message.chat.id, sent_msg.message_id)
        
        # Fallback to sending URL
        builder = InlineKeyboardBuilder()
        builder.button(text="Saytga o`tish", url=book_url)
        
        err_msg = f"⚙️ <b>Texnik sabablar tufayli \"{book_name}\" faylini Telegramga jo`natib bo`lmadi. (Masalan, fayl hajmi 50MB dan katta bo'lishi mumkin)</b>\n\n🔗 Quyidagi havola orqali Ziyouz saytining rasmiy sahifasida ushbu kitobdan foydalanishingiz mumkin.👇👇👇"
        await bot.send_message(chat_id=callback.from_user.id, text=err_msg, reply_markup=builder.as_markup())
        
        # Cleanup
        if os.path.exists(tmp_path):
            os.remove(tmp_path)