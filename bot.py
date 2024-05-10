from aiogram import Bot, Dispatcher
import asyncio
from handlers import (main_handlers, admin_handlers, faq_handlers,
                      call_request_handlers, services_handlers, appointment_handlers)

from dotenv import load_dotenv
import os

load_dotenv()

from middlewares.db import DataBaseSession
from database.engine import create_db, drop_db, session_maker


bot = Bot(token=os.getenv('BOT_TOKEN'), parse_mode="HTML")
dp = Dispatcher()

dp.include_router(main_handlers.router)
dp.include_router(admin_handlers.router)
dp.include_router(faq_handlers.router)
dp.include_router(call_request_handlers.router)
dp.include_router(appointment_handlers.router)
dp.include_router(services_handlers.router)


async def on_startup(bot):

    run_param = False
    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown(bot):
    print('Бот выключен')


async def main() -> None:
    dp.startup.register(on_startup)
    dp.startup.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await create_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
