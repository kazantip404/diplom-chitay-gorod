"""Страница корзины."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from config.config import TestConfig


class CartPage(BasePage):
    """Страница корзины."""

    def __init__(self, driver):
        super().__init__(driver)

    def manage_quantity(self) -> None:
        """Управление количеством товара."""
        self.logger.info("📊 Управление количеством товара")

        try:
            self.wait_for_page_load()

            # Кнопка увеличения (+)
            plus_button = self.safe_click(
                (By.CSS_SELECTOR, TestConfig.Selectors.QUANTITY_INCREMENT),
                description="Кнопка увеличения количества (+)"
            )
            self.logger.info("✅ Количество увеличено на +1")
            self.wait_for_page_load()
            self.wait_utils.wait_exact(1)

            # Кнопка уменьшения (-)
            minus_button = self.safe_click(
                (By.CSS_SELECTOR, TestConfig.Selectors.QUANTITY_DECREMENT),
                description="Кнопка уменьшения количества (-)"
            )
            self.logger.info("✅ Количество уменьшено на -1")

        except Exception as e:
            self.logger.warning(f"⚠️ Не удалось изменить количество: {e}")

    def clear_cart(self) -> None:
        """Очистка корзины."""
        self.logger.info("🗑️ Очистка корзины")

        try:
            clear_button = self.safe_click(
                (By.CSS_SELECTOR, TestConfig.Selectors.CLEAR_CART),
                description="Кнопка 'Очистить корзину'"
            )
            self.logger.info("✅ Корзина очищена")

            # Проверяем что корзина пуста
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, TestConfig.Selectors.EMPTY_CART_TEXT)
                    )
                )
                self.logger.info("✅ Подтверждение: корзина пуста")
            except TimeoutException:
                self.logger.info("ℹ️ Подтверждение очистки не найдено")

        except Exception as e:
            self.logger.warning(f"⚠️ Не удалось очистить корзину: {e}")

            # Альтернативный поиск
            try:
                clear_elements = self.driver.find_elements(
                    By.XPATH,
                    TestConfig.Selectors.CLEAR_CART_ALT
                )

                if clear_elements:
                    clear_elements[0].click()
                    self.logger.info("✅ Корзина очищена (альтернативный поиск)")
            except Exception:
                self.logger.info("ℹ️ Кнопка очистки не найдена")