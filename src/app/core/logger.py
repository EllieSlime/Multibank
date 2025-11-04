import sys
import os
from loguru import logger
from typing import Optional


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    rotation: str = "1 day",
    retention: str = "30 days",
    format_string: Optional[str] = None
) -> None:
    """
    Настройка логирования для приложения
    
    Args:
        log_level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Путь к файлу логов (если None, логи только в консоль)
        rotation: Ротация логов (например, "1 day", "100 MB")
        retention: Время хранения логов (например, "30 days", "10 files")
        format_string: Кастомный формат логов
    """
    
    logger.remove()
    
    if format_string is None:
        format_string = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
    
    logger.add(
        sys.stdout,
        format=format_string,
        level=log_level,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        logger.add(
            log_file,
            format=format_string,
            level=log_level,
            rotation=rotation,
            retention=retention,
            compression="zip",
            backtrace=True,
            diagnose=True
        )
    
    logger.disable("sqlalchemy.engine")
    logger.disable("sqlalchemy.pool")
    logger.disable("sqlalchemy.dialects")
    
    logger.enable("app")
    
    logger.info(f"Логирование настроено. Уровень: {log_level}")


def get_logger(name: str = None):
    """
    Получить логгер для модуля
    
    Args:
        name: Имя модуля (обычно __name__)
    
    Returns:
        Настроенный логгер
    """
    if name:
        return logger.bind(name=name)
    return logger


def setup_default_logging():
    """Настройка логирования по умолчанию"""
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_file = os.getenv("LOG_FILE", "logs/app.log")
    
    setup_logging(
        log_level=log_level,
        log_file=log_file,
        rotation="1 day",
        retention="30 days"
    )


# Экспортируем настроенный логгер
__all__ = ["logger", "setup_logging", "get_logger", "setup_default_logging"]
