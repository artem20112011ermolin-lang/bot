"""
Обработчики команд для администратора
"""
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_ID
import logging

logger = logging.getLogger(__name__)
router = Router()


class AdminStates(StatesGroup):
    waiting_for_photo = State()
    waiting_for_title = State()
    waiting_for_delete = State()


# Проверка: это админ?
def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


@router.message(Command("admin"))
async def cmd_admin_menu(message: Message):
    """Админ меню"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Доступ запрещён")
        return
    
    admin_menu = (
        "🔐 АДМИН ПАНЕЛЬ\n\n"
        "Управление портфолио:\n"
        "/add_work - Добавить новую работу\n"
        "/delete_work - Удалить работу\n"
        "/list_works - Список всех работ\n\n"
        "Выбери команду выше 👆"
    )
    await message.answer(admin_menu)


@router.message(Command("add_work"))
async def cmd_add_work(message: Message, state: FSMContext):
    """Начинает процесс добавления работы"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Доступ запрещён")
        return
    
    await message.answer(
        "📸 Загрузка новой работы\n\n"
        "Отправь фото для портфолио\n"
        "(Лучше всего в высоком качестве)"
    )
    await state.set_state(AdminStates.waiting_for_photo)


@router.message(AdminStates.waiting_for_photo, F.photo)
async def receive_photo(message: Message, state: FSMContext):
    """Получает фото"""
    file_id = message.photo[-1].file_id
    await state.update_data(file_id=file_id)
    await message.answer(
        "✅ Фото получено!\n\n"
        "Теперь введи название этой работы\n"
        "(например: 'Логотип компании' или 'Дизайн сайта')"
    )
    await state.set_state(AdminStates.waiting_for_title)


@router.message(AdminStates.waiting_for_title, F.text)
async def receive_title(message: Message, state: FSMContext, portfolio):
    """Получает название и сохраняет работу"""
    if not is_admin(message.from_user.id):
        await state.clear()
        return
    
    data = await state.get_data()
    file_id = data.get("file_id")
    title = message.text
    
    # Добавляем в портфолио
    success = portfolio.add_work(file_id, title)
    
    if success:
        count = portfolio.get_portfolio_count()
        await message.answer(
            f"✅ Работа успешно добавлена!\n\n"
            f"Название: {title}\n"
            f"Всего работ в портфолио: {count}\n\n"
            f"Теперь её видят пользователи!"
        )
    else:
        await message.answer(
            f"❌ Ошибка при добавлении работы\n\n"
            f"Возможная причина: работа с названием '{title}' уже существует"
        )
    
    await state.clear()


@router.message(Command("delete_work"))
async def cmd_delete_work(message: Message, state: FSMContext, portfolio):
    """Удаление работы"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Доступ запрещён")
        return
    
    count = portfolio.get_portfolio_count()
    if count == 0:
        await message.answer("❌ Портфолио пусто - нечего удалять")
        return
    
    works = portfolio.get_portfolio()
    works_list = "\n".join([f"#{i}. {w['title']}" for i, w in enumerate(works, 1)])
    
    delete_text = (
        f"Удаление работы\n\n"
        f"Текущие работы ({count} шт):\n\n"
        f"{works_list}\n\n"
        f"Введи номер работы (1-{count}) для удаления"
    )
    await message.answer(delete_text)
    await state.set_state(AdminStates.waiting_for_delete)


@router.message(AdminStates.waiting_for_delete, F.text)
async def confirm_delete(message: Message, state: FSMContext, portfolio):
    """Подтверждает удаление"""
    if not is_admin(message.from_user.id):
        await state.clear()
        return
    
    try:
        index = int(message.text)
        works = portfolio.get_portfolio()
        
        if index < 1 or index > len(works):
            await message.answer(f"❌ Номер должен быть от 1 до {len(works)}")
            return
        
        deleted_work = works[index - 1]
        success = portfolio.delete_work(index)
        
        if success:
            count = portfolio.get_portfolio_count()
            await message.answer(
                f"✅ Работа удалена!\n\n"
                f"Удалена: {deleted_work['title']}\n"
                f"Осталось работ: {count}"
            )
        else:
            await message.answer("❌ Ошибка при удалении")
    except ValueError:
        await message.answer("❌ Введи число! (например: 1, 2, 3)")
    finally:
        await state.clear()


@router.message(Command("list_works"))
async def cmd_list_works(message: Message, portfolio):
    """Показывает список всех работ"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Доступ запрещён")
        return
    
    count = portfolio.get_portfolio_count()
    
    if count == 0:
        await message.answer("📭 Портфолио пусто")
        return
    
    works = portfolio.get_portfolio()
    works_list = "\n".join([f"#{i}. {w['title']}" for i, w in enumerate(works, 1)])
    
    await message.answer(
        f"Портфолио ({count} {('работа' if count == 1 else 'работ')}):\n\n"
        f"{works_list}\n\n"
        f"Используй /delete_work для удаления"
    )


@router.message(AdminStates.waiting_for_photo)
async def invalid_photo(message: Message):
    """Если отправлено не фото"""
    await message.answer("❌ Пожалуйста, отправь фото (не документ, не видео)")
