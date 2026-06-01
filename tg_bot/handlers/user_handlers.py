"""
Обработчики команд для обычных пользователей
"""
from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from config import ABOUT_TEXT, CONTACTS_TELEGRAM, CONTACTS_VK, FUNPAY_LINK
from utils.keyboards import main_keyboard, get_back_button, portfolio_navigation
import logging

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Команда /start"""
    welcome_text = (
        "👋 *Привет! Добро пожаловать в мою дизайн-студию!*\n\n"
        "Я профессиональный дизайнер с опытом в различных направлениях.\n\n"
        "Что я здесь предлагаю:\n"
        "🎨 Посмотреть мои работы\n"
        "💼 Оформить заказ\n"
        "📱 Мои контакты\n"
        "ℹ️ Подробнее обо мне\n\n"
        "Выбери, что тебя интересует 👇"
    )
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=main_keyboard())


@router.callback_query(F.data == "portfolio")
async def show_portfolio(callback: CallbackQuery, state: FSMContext, portfolio):
    """Показывает портфолио"""
    works = portfolio.get_portfolio()
    
    if not works:
        await callback.answer("📭 Портфолио пока пусто. Скоро добавлю новые работы!", show_alert=True)
        return
    
    # Отправляем первую работу
    first_work = works[0]
    caption = f"📌 *{first_work['title']}*\n\n[{1}/{len(works)}] работ в портфолио"
    
    try:
        await callback.message.delete()
        await callback.message.answer_photo(
            photo=first_work["file_id"],
            caption=caption,
            parse_mode="Markdown",
            reply_markup=portfolio_navigation() if len(works) > 1 else get_back_button()
        )
        # Сохраняем индекс текущей работы в состояние
        await state.update_data(current_portfolio_index=0, portfolio_list=works)
    except Exception as e:
        logger.error(f"Ошибка отправки фото портфолио: {e}")
        await callback.answer("❌ Ошибка при загрузке фото", show_alert=True)
        return
    
    await callback.answer()


@router.callback_query(F.data == "portfolio_next")
async def show_next_portfolio(callback: CallbackQuery, state: FSMContext):
    """Показывает следующую работу"""
    data = await state.get_data()
    current_index = data.get("current_portfolio_index", 0)
    works = data.get("portfolio_list", [])
    
    if not works:
        await callback.answer()
        return
    
    # Переходим к следующей (циклично)
    next_index = (current_index + 1) % len(works)
    work = works[next_index]
    
    caption = f"📌 *{work['title']}*\n\n[{next_index + 1}/{len(works)}] работ в портфолио"
    
    try:
        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=work["file_id"],
                caption=caption,
                parse_mode="Markdown"
            ),
            reply_markup=portfolio_navigation() if len(works) > 1 else get_back_button()
        )
        await state.update_data(current_portfolio_index=next_index)
    except Exception as e:
        logger.error(f"Ошибка при переключении работы: {e}")
        await callback.answer("❌ Ошибка", show_alert=True)
    
    await callback.answer()


@router.callback_query(F.data == "portfolio_prev")
async def show_prev_portfolio(callback: CallbackQuery, state: FSMContext):
    """Показывает предыдущую работу"""
    data = await state.get_data()
    current_index = data.get("current_portfolio_index", 0)
    works = data.get("portfolio_list", [])
    
    if not works:
        await callback.answer()
        return
    
    # Переходим к предыдущей (циклично)
    prev_index = (current_index - 1) % len(works)
    work = works[prev_index]
    
    caption = f"📌 *{work['title']}*\n\n[{prev_index + 1}/{len(works)}] работ в портфолио"
    
    try:
        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=work["file_id"],
                caption=caption,
                parse_mode="Markdown"
            ),
            reply_markup=portfolio_navigation() if len(works) > 1 else get_back_button()
        )
        await state.update_data(current_portfolio_index=prev_index)
    except Exception as e:
        logger.error(f"Ошибка при переключении работы: {e}")
        await callback.answer("❌ Ошибка", show_alert=True)
    
    await callback.answer()


@router.callback_query(F.data == "order")
async def show_order(callback: CallbackQuery):
    """Показывает ссылку на заказ"""
    order_text = (
        "🛒 *Заказать дизайн*\n\n"
        "Я готов воплотить твои идеи в жизнь! 🚀\n\n"
        "*Мой опыт:*\n"
        "✨ Логотипы и фирменный стиль\n"
        "📱 Дизайн интерфейсов (UI/UX)\n"
        "🌐 Веб-дизайн и макеты\n"
        "🎨 Графический дизайн\n"
        "📸 Обработка и ретушь фото\n"
        "💼 Брендинг под ключ\n\n"
        "💰 *Стоимость:* зависит от сложности проекта\n"
        "⏱️ *Сроки:* обсуждаем индивидуально\n\n"
        f"[📥 Оформить заказ на FunPay]({FUNPAY_LINK})\n\n"
        f"Или свяжись со мной: {CONTACTS_TELEGRAM}"
    )
    
    await callback.message.edit_text(
        order_text,
        parse_mode="Markdown",
        reply_markup=get_back_button()
    )
    await callback.answer()


@router.callback_query(F.data == "contacts")
async def show_contacts(callback: CallbackQuery):
    """Показывает контакты"""
    contacts_text = (
        "📱 *Как со мной связаться?*\n\n"
        f"🔵 *Telegram:* [{CONTACTS_TELEGRAM}](https://t.me/fufawinher)\n"
        f"💙 *ВКонтакте:* [{CONTACTS_VK}]({CONTACTS_VK})\n"
        f"🏪 *FunPay:* [{FUNPAY_LINK}]({FUNPAY_LINK})\n\n"
        "*Я отвечаю:*\n"
        "⚡ В течение часа (в рабочее время)\n"
        "💬 На все вопросы и предложения\n"
        "🎯 С готовностью помочь и подсказать\n\n"
        "_Готов обсудить твой проект! 😊_"
    )
    
    await callback.message.edit_text(
        contacts_text,
        parse_mode="Markdown",
        reply_markup=get_back_button()
    )
    await callback.answer()


@router.callback_query(F.data == "about")
async def show_about(callback: CallbackQuery):
    """Показывает информацию обо мне"""
    about_text = f"ℹ️ *Обо мне*\n\n{ABOUT_TEXT}"
    
    await callback.message.edit_text(
        about_text,
        parse_mode="Markdown",
        reply_markup=get_back_button()
    )
    await callback.answer()


@router.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery, state: FSMContext):
    """Возвращает в главное меню"""
    await state.clear()
    welcome_text = (
        "👋 *Добро пожаловать в мою дизайн-студию!*\n\n"
        "Выбери, что тебя интересует 👇"
    )
    await callback.message.edit_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )
    await callback.answer()
