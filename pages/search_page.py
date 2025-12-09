"""
Page Object для поиска
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage  # <-- ТОЧКА!
import allure
import logging
import time

logger = logging.getLogger(__name__)


class SearchPage(BasePage):
    """Страница поиска"""

    # Локаторы
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.search-form__input")
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".product-card, .catalog-product")

    @allure.step("Поиск товара '{query}'")
    def search_product(self, query):
        """Выполнить поиск товара"""
        logger.info(f"🔍 Поиск: {query}")

        search_input = self.safe_find_element(
            *self.SEARCH_INPUT,
            description="Поле поиска"
        )
        search_input.clear()
        search_input.send_keys(query)
        search_input.send_keys(Keys.RETURN)

        # Ждем результаты
        self.wait_for_page_load()
        logger.info("✅ Результаты поиска загружены")

    @allure.step("Выбрать первую книгу с 'Война и мир'")
    def select_first_book(self):
        """Выбрать книгу из результатов"""
        logger.info("📚 Выбор книги")

        book_selectors = [
            (By.XPATH, "//a[contains(., 'Война и мир') and contains(., 'Книга 2')]"),
            (By.XPATH, "//a[contains(., 'Война и мир')]"),
            (By.CSS_SELECTOR, ".product-card a")
        ]

        for selector_type, selector_value in book_selectors:
            try:
                self.safe_click(
                    (selector_type, selector_value),
                    description=f"Книга по селектору {selector_value}"
                )
                logger.info(f"✅ Нажата книга по селектору: {selector_value}")

                self.wait_for_page_load()
                return True
            except:
                continue

        raise Exception("❌ Не удалось выбрать книгу")