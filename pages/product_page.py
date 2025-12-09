"""Страница товара."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
from config.config import TestConfig


class ProductPage(BasePage):
    """Страница товара."""

    def __init__(self, driver):
        super().__init__(driver)

    def add_to_cart(self) -> None:
        """Добавление товара в корзину."""
        self.logger.info("🛒 Добавление в корзину")

        buy_button = self.safe_click(
            (By.CSS_SELECTOR, TestConfig.Selectors.BUY_BUTTON),
            description="Кнопка 'Купить'"
        )
        self.logger.info("✅ Товар добавлен в корзину")

    def go_to_cart(self) -> None:
        """Переход в корзину."""
        self.logger.info("📦 Переход в корзину")

        # Проверяем изменилась ли кнопка на "Оформить"
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: "Оформить" in d.find_element(
                    By.CSS_SELECTOR, TestConfig.Selectors.CHECKOUT_BUTTON
                ).text
            )
            self.logger.info("✅ Кнопка изменилась на 'Оформить'")

            self.safe_click(
                (By.CSS_SELECTOR, TestConfig.Selectors.CHECKOUT_BUTTON),
                description="Кнопка 'Оформить'"
            )

        except TimeoutException:
            # Если кнопка не изменилась, ищем иконку корзины
            self.logger.info("ℹ️ Кнопка не изменилась, ищем иконку корзины")

            try:
                cart_icon = self.safe_click(
                    (By.CSS_SELECTOR, TestConfig.Selectors.CART_ICON),
                    description="Иконка корзины"
                )
            except Exception:
                # Прямой переход по URL
                self.logger.info("ℹ️ Переход по прямому URL корзины")
                self.driver.get(TestConfig.CART_URL)

        self.wait_for_page_load()