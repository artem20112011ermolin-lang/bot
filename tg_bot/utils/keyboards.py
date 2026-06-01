"""
Клавиатуры (inline buttons)
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_keyboard() -> InlineKeyboardMarkup:
    """Главная клавиатура"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎨 Портфолио", callback_data="portfolio")],
            [InlineKeyboardButton(text="🛒 Заказать", callback_data="order")],
            [InlineKeyboardButton(text="📱 Контакты", callback_data="contacts")],
            [InlineKeyboardButton(text="ℹ️ Обо мне", callback_data="about")],
        ]
    )
    return keyboard


def get_back_button() -> InlineKeyboardMarkup:
    """Кнопка 'Назад в меню'"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")],
        ]
    )
    return keyboard


def portfolio_navigation() -> InlineKeyboardMarkup:
    """Навигация по портфолио"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="prev_work"),
                InlineKeyboardButton(text="Вперёд ➡️", callback_data="next_work"),
            ],
            [InlineKeyboardButton(text="🏠 Меню", callback_data="back")],
        ]
    )
    return keyboard
