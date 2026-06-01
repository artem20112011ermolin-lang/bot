"""
Главный файл Telegram-бота для дизайнера-фрилансера
"""
import asyncio
import logging
from aiogram import Dispatcher, Bot, BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.fsm.storage.memory import MemoryStorage
from config import TELEGRAM_BOT_TOKEN, ADMIN_ID, PORTFOLIO_FILE
from utils.sheets_manager import PortfolioManager
from handlers import user_handlers, admin_handlers

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PortfolioMiddleware(BaseMiddleware):
    """Middleware для передачи портфолио менеджера во все обработчики"""
    
    def __init__(self, portfolio: PortfolioManager):
        self.portfolio = portfolio
        super().__init__()
    
    async def __call__(self, handler, event: TelegramObject, data: dict):
        data["portfolio"] = self.portfolio
        return await handler(event, data)


async def main():
    """Главная функция запуска бота"""
    
    # Инициализируем бота с хранилищем состояний
    storage = MemoryStorage()
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(storage=storage)
    
    # Инициализируем менеджер портфолио
    portfolio = PortfolioManager(storage_file=str(PORTFOLIO_FILE))
    logger.info("✅ Менеджер портфолио инициализирован")
    
    # Регистрируем middleware
    dp.message.middleware(PortfolioMiddleware(portfolio))
    dp.callback_query.middleware(PortfolioMiddleware(portfolio))
    
    # Регистрируем роутеры (обработчики)
    dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)
    
    logger.info("=" * 60)
    logger.info("🎨 БОТ ДИЗАЙНЕРА ЗАПУЩЕН И ГОТОВ К РАБОТЕ!")
    logger.info("=" * 60)
    logger.info(f"👤 Admin ID: {ADMIN_ID}")
    logger.info(f"📁 Портфолио: {PORTFOLIO_FILE}")
    logger.info(f"🤖 Бот работает в режиме polling...")
    logger.info("=" * 60)
    
    try:
        # Запуск polling
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types()
        )
    except KeyboardInterrupt:
        logger.info("🛑 Бот остановлен пользователем")
    finally:
        await bot.session.close()
        logger.info("✅ Сессия закрыта")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен")

