# config/__init__.py - УПРОЩЕННЫЙ ВАРИАНТ
"""
Единая точка входа для конфигурации
Упрощенный вариант для минимизации ошибок
"""

# Экспортируем ВСЕ из settings и tokens
from .settings import *
from .tokens import *


# Для обратной совместимости с from config import Config
class Config:
    """Для обратной совместимости"""
    BASE_URL = BASE_URL
    API_BASE_URL = API_BASE_URL
    TIMEOUT = TIMEOUT
    DEFAULT_CITY_ID = DEFAULT_CITY_ID
    TEST_AUTH_TOKEN = AUTH_TOKEN if 'AUTH_TOKEN' in locals() else ""


class TestData:
    """Для обратной совместимости"""
    TEST_PHRASES = TEST_DATA.get("SEARCH_PHRASES", [])
    TEST_PRODUCTS = TEST_DATA.get("TEST_PRODUCTS", [])
    CITIES = TEST_DATA.get("CITIES", {})

    # Для обратной совместимости с test_ui.py
    TEST_PRODUCTS = ["Лев Толстой", "Достоевский", "Пушкин", "Чехов"]


class Selectors:
    """Для обратной совместимости"""
    SEARCH_INPUT = SELECTORS.get("SEARCH_INPUT", "input.search-form__input")
    COOKIE_BUTTON = SELECTORS.get("COOKIE_BUTTON", "//button[contains(., 'Принять')]")
    PRODUCT_CARD = SELECTORS.get("PRODUCT_CARD", ".product-card")
    BUY_BUTTON = SELECTORS.get("BUY_BUTTON", "button.product-buttons__main-action")