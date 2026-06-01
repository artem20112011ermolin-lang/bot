"""
Менеджер для локального хранилища портфолио (JSON файл)
"""
import json
from pathlib import Path
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class PortfolioManager:
    """Менеджер портфолио с сохранением в JSON"""
    
    def __init__(self, storage_file: str = "data/portfolio.json"):
        """
        Инициализирует менеджер портфолио
        
        Args:
            storage_file: Путь к JSON файлу для хранения работ
        """
        self.storage_file = Path(storage_file)
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Создаём файл если не существует
        if not self.storage_file.exists():
            self.storage_file.write_text(json.dumps([], indent=2, ensure_ascii=False))
            logger.info(f"Создан файл портфолио: {self.storage_file}")

    def get_portfolio(self) -> List[Dict[str, str]]:
        """
        Получает всё портфолио
        
        Returns:
            Список словарей с ключами 'file_id' и 'title'
        """
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                portfolio = json.load(f)
            return portfolio
        except Exception as e:
            logger.error(f"Ошибка чтения портфолио: {e}")
            return []

    def add_work(self, file_id: str, title: str) -> bool:
        """
        Добавляет новую работу
        
        Args:
            file_id: Telegram file_id фото
            title: Название работы
            
        Returns:
            True если успешно, False если ошибка
        """
        try:
            portfolio = self.get_portfolio()
            
            # Проверяем дублирование
            if any(work['title'] == title for work in portfolio):
                logger.warning(f"Работа с названием '{title}' уже существует")
                return False
            
            # Добавляем новую работу
            new_work = {
                "file_id": file_id,
                "title": title
            }
            portfolio.append(new_work)
            
            # Сохраняем
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(portfolio, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Добавлена работа: {title}")
            return True
        except Exception as e:
            logger.error(f"Ошибка добавления работы: {e}")
            return False

    def delete_work(self, index: int) -> bool:
        """
        Удаляет работу по индексу (1-based)
        
        Args:
            index: Номер работы (начиная с 1)
            
        Returns:
            True если успешно, False если ошибка
        """
        try:
            portfolio = self.get_portfolio()
            
            # Проверяем валидность индекса
            if index < 1 or index > len(portfolio):
                logger.warning(f"Неверный индекс: {index}")
                return False
            
            # Удаляем работу (индекс 1-based)
            removed = portfolio.pop(index - 1)
            
            # Сохраняем
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(portfolio, f, indent=2, ensure_ascii=False)
            
            logger.info(f"🗑️ Удалена работа: {removed['title']}")
            return True
        except Exception as e:
            logger.error(f"Ошибка удаления работы: {e}")
            return False

    def get_portfolio_count(self) -> int:
        """Получает количество работ"""
        try:
            return len(self.get_portfolio())
        except Exception as e:
            logger.error(f"Ошибка получения количества работ: {e}")
            return 0

