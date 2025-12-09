"""Конфигурация тестовых данных."""


class TestConfig:
    """Основная конфигурация тестов."""

    # URL
    BASE_URL = "https://www.chitai-gorod.ru"
    CART_URL = f"{BASE_URL}/cart/"

    # Тестовые данные
    SEARCH_QUERY = "Лев Толстой Война и мир"
    BOOK_TITLE = "Война и мир"

    # Таймауты
    TIMEOUT = 10
    IMPLICIT_WAIT = 3
    PAGE_LOAD_TIMEOUT = 30

    # Селекторы элементов
    class Selectors:
        """Селекторы элементов."""

        # Куки
        COOKIE_BUTTON = "//button[contains(., 'Принять') or contains(., 'Согласен')]"

        # Поиск
        SEARCH_INPUT = "input.search-form__input"

        # Карточки товара
        PRODUCT_CARD = ".product-card a"
        BOOK_LINK = "//a[contains(., 'Война и мир')]"
        BOOK_LINK_EXACT = "//a[contains(., 'Война и мир') and contains(., 'Книга 2')]"

        # Кнопки товара
        BUY_BUTTON = "button.product-buttons__main-action"
        CHECKOUT_BUTTON = "button.product-buttons__main-action"

        # Корзина
        CART_ICON = "a[href*='/cart/'], .header-cart"
        QUANTITY_INCREMENT = ".chg-ui-input-number__input-control--increment"
        QUANTITY_DECREMENT = ".chg-ui-input-number__input-control--decrement"
        CLEAR_CART = "#__nuxt > div > div.app-wrapper__content > div.app-wrapper__container > div > div > div > div.cart-page__head > div > div.cart-page__delete-many > span"
        CLEAR_CART_ALT = "//*[contains(., 'Очистить корзину')]"
        EMPTY_CART_TEXT = "//*[contains(., 'корзина пуста') or contains(., 'Корзина пуста')]"