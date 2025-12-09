from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure


class BookPage(BasePage):
    """📖 СТРАНИЦА КОНКРЕТНОЙ КНИГИ"""

    # 🎯 ЛОКАТОРЫ ДЛЯ СТРАНИЦЫ КНИГИ - ПОДСТАВЬ РЕАЛЬНЫЕ

    # 📝 ИНФОРМАЦИЯ О КНИГЕ
    BOOK_TITLE = (By.CSS_SELECTOR, "h1, .book-title, .product-title")
    AUTHOR_NAME = (By.CSS_SELECTOR, ".author, .book-author, .product-author")
    PRICE = (By.CSS_SELECTOR, ".price, .book-price, .product-price")

    # 🛒 КНОПКА ДОБАВЛЕНИЯ В КОРЗИНУ
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, ".add-to-cart, .buy-btn, .to-cart")

    # ✅ СООБЩЕНИЕ О ДОБАВЛЕНИИ В КОРЗИНУ
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-message, .added-to-cart, .alert-success")

    @allure.step("Получить название книги")
    def get_book_title(self):
        """📖 Получить название книги со страницы"""
        return self.get_text(self.BOOK_TITLE)

    @allure.step("Получить автора книги")
    def get_author(self):
        """✍️ Получить имя автора книги"""
        return self.get_text(self.AUTHOR_NAME) if self.is_visible(self.AUTHOR_NAME) else ""

    @allure.step("Добавить книгу в корзину")
    def add_to_cart(self):
        """🛒 Добавить текущую книгу в корзину"""
        self.click(self.ADD_TO_CART_BTN)
        # ✅ Проверяем, что появилось сообщение об успешном добавлении
        return self.is_visible(self.SUCCESS_MESSAGE, timeout=5)