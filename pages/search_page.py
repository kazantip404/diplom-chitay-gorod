"""Страница поиска."""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from config.config import TestConfig


class SearchPage(BasePage):
    """Страница поиска товаров."""

    def __init__(self, driver):
        super().__init__(driver)

    def search_product(self, query: str = TestConfig.SEARCH_QUERY) -> None:
        """Поиск товара."""
        self.logger.info(f"🔍 Поиск товара: {query}")

        # Находим поле поиска
        search_input = self.safe_find_element(
            By.CSS_SELECTOR,
            TestConfig.Selectors.SEARCH_INPUT,
            description="Поле поиска"
        )

        # Вводим запрос
        search_input.clear()
        search_input.send_keys(query)
        search_input.send_keys(Keys.RETURN)
        self.logger.info("✅ Поиск выполнен")
        self.wait_for_page_load()

    def select_book(self, exact_match: bool = True) -> bool:
        """Выбор книги из результатов поиска."""
        self.logger.info("📚 Выбор книги из результатов")

        found_book = False

        if exact_match:
            # Способ 1: Ищем по точному тексту
            try:
                book_elements = self.driver.find_elements(
                    By.XPATH,
                    TestConfig.Selectors.BOOK_LINK_EXACT
                )

                for element in book_elements:
                    if element.is_displayed():
                        book_link = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, TestConfig.Selectors.BOOK_LINK_EXACT)
                            )
                        )
                        book_link.click()
                        found_book = True
                        self.logger.info("✅ Найдена книга 'Война и мир. Книга 2'")
                        break
            except Exception:
                pass

        if not found_book:
            # Способ 2: Ищем по частичному совпадению
            try:
                war_and_peace_links = self.driver.find_elements(
                    By.XPATH,
                    TestConfig.Selectors.BOOK_LINK
                )

                if war_and_peace_links:
                    book_link = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, TestConfig.Selectors.BOOK_LINK)
                        )
                    )
                    book_link.click()
                    found_book = True
                    self.logger.info("✅ Найдена книга с 'Война и мир' в названии")
            except Exception:
                pass

        if not found_book:
            # Способ 3: Берем первую карточку товара
            try:
                first_product = self.safe_click(
                    (By.CSS_SELECTOR, TestConfig.Selectors.PRODUCT_CARD),
                    description="Первая карточка товара"
                )
                found_book = True
                self.logger.info("✅ Открыта первая карточка товара")
            except Exception:
                self.logger.error("❌ Не удалось найти ни одной книги")
                raise

        self.wait_for_page_load()
        return found_book