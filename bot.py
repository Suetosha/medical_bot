from aiogram import Bot, Dispatcher
import asyncio
from handlers import (main_handlers, admin_handlers, faq_handlers,
                      call_request_handlers, services_handlers, appointment_handlers, slots_handlers)

from dotenv import load_dotenv
import os

load_dotenv()

from middlewares.db import DataBaseSession
from database.engine import sync_db, drop_db, session_maker


bot = Bot(token=os.getenv('BOT_TOKEN'), parse_mode="HTML")
dp = Dispatcher()


# Регистрация роутеров для связи с хэндлерами
dp.include_router(main_handlers.router)
dp.include_router(admin_handlers.router)
dp.include_router(faq_handlers.router)
dp.include_router(call_request_handlers.router)
dp.include_router(appointment_handlers.router)
dp.include_router(services_handlers.router)
dp.include_router(slots_handlers.router)


async def on_startup():

    # Если параметр clear_db = True, то очищается база
    clear_db = False
    if clear_db:
        # Используется для удаления всех таблиц базы данных
        await drop_db()

    # Используется для синхронизации моделей с базой данных
    await sync_db()
    print('Бот включен')


async def on_shutdown():
    print('Бот выключен')


async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
