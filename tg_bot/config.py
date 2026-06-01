"""
Конфигурация Telegram-бота
Переменные окружения загружаются из .env файла
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Загружаем переменные из .env файла
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# ===== TELEGRAM =====
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# ===== ТЕКСТ ОПИСАНИЙ =====
ABOUT_TEXT = """Привет! Я дизайнер из СНГ с 3+ годами опыта в Photoshop и современном дизайне.

Мою специализацию:
🎨 Графический дизайн
📱 Дизайн интерфейсов (UI)
🌐 Веб-дизайн
✨ Брендинг и логотипы
📸 Обработка фото

Все работы делаю сам, качественно и в срок. Каждый проект - это внимание к деталям и творческий подход.

Доверь свой проект профессионалу! 💪"""

# ===== КОНТАКТЫ =====
CONTACTS_TELEGRAM = "@fufawinher"
CONTACTS_VK = "https://vk.com/club238603550"
FUNPAY_LINK = "https://funpay.com/lots/offer?id=70101718"

# ===== ЛОКАЛЬНОЕ ХРАНИЛИЩЕ =====
PORTFOLIO_FILE = Path(__file__).parent / "data" / "portfolio.json"

# ===== ВАЛИДАЦИЯ =====
if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
    print("⚠️  TELEGRAM_BOT_TOKEN не установлен в .env файле")

if ADMIN_ID == 0:
    print("⚠️  ADMIN_ID не установлен в .env файле")


