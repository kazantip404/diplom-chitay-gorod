# config/settings.py - ДОБАВЬТЕ SELECTORS
"""
Основные настройки проекта
"""

# Базовые URL
BASE_URL = "https://www.chitai-gorod.ru"
API_BASE_URL = "https://web-agr.chitai-gorod.ru"
TIMEOUT = 15
DEFAULT_CITY_ID = 213  # Москва

# Пути API
PUBLIC_API_ENDPOINTS = {
    "SEARCH_PRODUCT": "/web/api/v2/search/product",
    "POPULAR_SEARCHES": "/web/api/v2/search/popular-search-phrases",
    "SEARCH_SUGGESTS": "/web/api/v2/search/search-phrase-suggests",
    "FACET_SEARCH": "/web/api/v2/search/facet-search",
}

PROTECTED_API_ENDPOINTS = {
    "CART_SHORT": "/web/api/v1/cart/short",
    "ORDERS": "/web/api/v2/orders",
    "ORDER_INFO": "/web/api/v2/order-info/by-last-order",
}

# Тестовые данные
TEST_DATA = {
    "SEARCH_PHRASES": ["Лев Толстой", "роман", "книга", "детектив", "фантастика"],
    "TEST_PRODUCTS": ["Лев Толстой", "Достоевский", "Пушкин", "Чехов"],
    "CITIES": {"Москва": 213, "Санкт-Петербург": 2, "Новосибирск": 65}
}

# CSS селекторы для UI тестов - ДОБАВЛЕНО!
SELECTORS = {
    "SEARCH_INPUT": "input.search-form__input",
    "COOKIE_BUTTON": "//button[contains(., 'Принять') or contains(., 'Согласен')]",
    "PRODUCT_CARD": ".product-card",
    "BUY_BUTTON": "button.product-buttons__main-action"
}