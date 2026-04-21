import asyncio
import logging

from loader import dp, db, bot
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
import middlewares, handlers

async def main():
    logging.basicConfig(level=logging.INFO)
    
    # Initialize Database table
    try:
        await db.create_table_users()
    except Exception as err:
        logging.error(f"Error creating table: {err}")

    # Set up bot commands
    await set_default_commands(bot)
    
    # Notify admins
    await on_startup_notify(bot)
    
    # Start polling
    logging.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
