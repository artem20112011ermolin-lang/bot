# 🤖 Telegram-Бот для Дизайнера

Полнофункциональный Telegram-бот на Python + aiogram 3.x для фрилансера-дизайнера. **Без внешних зависимостей** - всё работает локально!

## 🎯 Функции

### Для пользователей:
- **Портфолио** - просмотр работ (фото хранятся в памяти бота)
- **Заказать** - ссылка на FunPay
- **Контакты** - соцсети
- **Обо мне** - информация о дизайнере

### Для администратора (только твой ID):
- `/add_work` - добавить новую работу (фото + название)
- `/delete_work` - удалить работу по номеру
- `/list_works` - список всех работ
- `/admin` - админ-панель

---

## ⚙️ Быстрая установка

### 1. Требования
```
Python 3.10+
pip
Telegram аккаунт
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Получение Telegram Bot Token

1. Откройте Telegram и найдите **@BotFather**
2. Отправьте `/newbot`
3. Следуйте инструкциям, скопируйте токен
4. Вставьте в файл `.env`:
   ```
   TELEGRAM_BOT_TOKEN=123456789:ABCDefGhIjKlMnOpQrStUvWxYz
   ```

### 4. Получение своего Telegram ID

1. Найдите бота **@userinfobot**
2. Отправьте ему любое сообщение
3. Скопируйте ID и вставьте в `.env`:
   ```
   ADMIN_ID=987654321
   ```

### 5. Запуск! 🚀
```bash
python main.py
```

Если видишь:
```
✅ Менеджер портфолио инициализирован
🤖 Бот запущен!
👤 Admin ID: 987654321
📁 Портфолио: data/portfolio.json
```

**ТЫ ГОТОВ!** Найди своего бота и напиши `/start`

---

## 📁 Структура проекта

```
tg_bot/
├── main.py                 # Главный файл бота
├── config.py              # Конфигурация
├── requirements.txt       # Зависимости (только 2 пакета!)
├── .env                   # Переменные окружения
├── .gitignore            # Исключения для git
│
├── data/
│   └── portfolio.json     # Локальное хранилище работ
│
├── handlers/
│   ├── __init__.py
│   ├── user_handlers.py   # Обработчики пользователей
│   └── admin_handlers.py  # Обработчики админа
│
└── utils/
    ├── __init__.py
    ├── keyboards.py       # Inline кнопки
    └── sheets_manager.py  # Менеджер портфолио
```

---

## 🎮 Использование

### Для пользователей:
1. Найди бота в Telegram (по username)
2. Отправь `/start`
3. Используй кнопки для навигации

### Для админа (твой ID):
1. `/add_work` → отправь фото → напиши название
2. `/delete_work` → выбери номер для удаления
3. `/list_works` → посмотри все работы

---

## 💾 Хранилище данных

Работы хранятся в **JSON файле** `data/portfolio.json`:

```json
[
  {
    "file_id": "AgADBAADr...",
    "title": "Логотип компании"
  },
  {
    "file_id": "AgADBAADt...",
    "title": "Дизайн сайта"
  }
]
```

**Без Google Sheets, без облака** - всё локально! ✨

---

## 🔧 Кастомизация

### Изменить текст "Обо мне":
```python
# config.py
ABOUT_TEXT = "Твой текст здесь"
```

### Изменить ссылку FunPay:
```python
# config.py
FUNPAY_LINK = "https://funpay.com/users/ТВИ_НИК/"
```

### Изменить Telegram контакты:
```python
# config.py
CONTACTS_TELEGRAM = "@ТВИ_ТГ"
```

---

## 🚀 Где захостить бота?

### Вариант 1: **Replit** (САМЫЙ ПРОСТОЙ) ⭐
- Бесплатно, работает 24/7
- Не нужна карта (условно)
- Шаги:
  1. Перейди на https://replit.com/
  2. Sign up (можно через Google)
  3. Create → Import from GitHub
  4. Вставь ссылку: `https://github.com/твой_юзер/tg_bot`
  5. В Replit создай `.env` файл с переменными
  6. Запусти `python main.py`

### Вариант 2: **PythonAnywhere** (тоже просто)
- Бесплатный тарифф с ограничениями
- https://www.pythonanywhere.com/
- Шаги: залей файлы → создай Web app → запусти скрипт

### Вариант 3: **VPS/Сервер** (продвинутый)
- **Hetzner** - дешевле всех (~2$/мес за VPS)
- **DigitalOcean** - популярный (~4$/мес)
- **AWS** - мощный но сложнее
- Как запустить там:
  1. SSH на сервер
  2. `git clone` твой репо
  3. `pip install -r requirements.txt`
  4. `nohup python main.py > bot.log 2>&1 &` (запуск в фоне)

### Вариант 4: **Telegram Bot API Webhook** (продвинутый)
Вместо polling используй webhook:
```python
# Добавь в main.py
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# ... вместо dp.start_polling()
```

### Вариант 5: **Docker + любой сервер** (кому лень)
Создай `Dockerfile`:
```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

Потом `docker run -e TELEGRAM_BOT_TOKEN=... tg_bot`

---

## ❓ FAQ

**Q: Как сделать так, чтобы бот работал 24/7?**  
A: Захости на Replit, PythonAnywhere или VPS

**Q: Где хранятся фото?**  
A: Telegram хранит фото, а ID сохраняется в `data/portfolio.json`

**Q: Можно ли несколько админов?**  
A: Да, измени config.py (замени `ADMIN_ID` на список)

**Q: Что если потеряю file_id?**  
A: Фото всегда на Telegram серверах, просто попроси админа заново добавить

**Q: Безопасно ли?**  
A: Да, токены в `.env` файле, не отправляются никуда

---

## 🐛 Решение проблем

**"ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**"Invalid token"**
- Скопируй токен заново от @BotFather
- Убедись, что нет пробелов в начале/конце

**"Бот не отвечает"**
- Проверь интернет
- Перезагрузи бота (Ctrl+C, потом запусти заново)
- Посмотри логи в консоли

**ADMIN_ID не работает**
```bash
# Проверь правильность ID
# @userinfobot должен вернуть число без букв
```

---

## 📞 Поддержка

Если что-то не работает:
1. Посмотри логи в консоли
2. Проверь `.env` файл
3. Убедись, что все переменные установлены
4. Перезагрузи бота

---

## 📦 Требования

Минимум зависимостей:
- `aiogram==3.4.1` - фреймворк для ботов
- `python-dotenv==1.0.0` - загрузка переменных окружения

Всё! Больше ничего не нужно!

---

**Статус**: ✅ Готово к использованию

Дата создания: Июнь 2026  
Версия: 2.0 (без Google Sheets)  
Python: 3.10+  
Aiogram: 3.4.1

