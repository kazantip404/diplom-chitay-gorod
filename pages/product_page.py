"""
Page Object для страницы товара
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage  # <-- ТОЧКА!
import allure
import logging
import time

logger = logging.getLogger(__name__)


class ProductPage(BasePage):
    """Страница товара"""

    # Локаторы
    BUY_BUTTON = (By.CSS_SELECTOR, "button.product-buttons__main-action")
    CHECKOUT_BUTTON = (By.XPATH, "//button[contains(., 'Оформить')]")
    CART_ICON = (By.CSS_SELECTOR, "a[href*='cart'], .header-cart")

    @allure.step("Нажать кнопку 'Купить'")
    def click_buy_button(self):
        """Нажать кнопку 'Купить' или 'В корзину'"""
        logger.info("🛒 Поиск кнопки 'Купить'")

        button_selectors = [
            (By.CSS_SELECTOR, "button.product-buttons__main-action"),
            (By.XPATH, "//button[contains(., 'Купить')]"),
            (By.XPATH, "//button[contains(., 'В корзину')]"),
        ]

        for selector_type, selector_value in button_selectors:
            try:
                button = self.safe_click(
                    (selector_type, selector_value),
                    description=f"Кнопка по селектору {selector_value}"
                )

                button_text = button.text.lower()
                logger.info(f"✅ Нажата кнопка: {button_text}")

                # Ждем изменения кнопки
                try:
                    self.wait.until(
                        EC.text_to_be_present_in_element(
                            (By.CSS_SELECTOR, "button.product-buttons__main-action"),
                            "Оформить"
                        )
                    )
                    logger.info("✅ Кнопка изменилась на 'Оформить'")
                except:
                    logger.info("ℹ️ Кнопка не изменилась")

                return True
            except:
                continue

        logger.error("❌ Не удалось найти кнопку 'Купить'")
        return False

    @allure.step("Перейти к оформлению заказа")
    def proceed_to_checkout(self):
        """Нажать 'Оформить' или перейти в корзину"""
        logger.info("📦 Переход к оформлению")

        # Пробуем кнопку 'Оформить'
        try:
            self.safe_click(
                self.CHECKOUT_BUTTON,
                description="Кнопка 'Оформить'"
            )
            logger.info("✅ Нажата кнопка 'Оформить'")
            return True
        except:
            # Пробуем иконку корзины
            try:
                self.safe_click(
                    self.CART_ICON,
                    description="Иконка корзины"
                )
                logger.info("✅ Нажата иконка корзины")
                return True
            except:
                # Прямой переход по URL
                logger.info("ℹ️ Переход по прямому URL корзины")
                self.driver.get("https://www.chitai-gorod.ru/cart/")
                self.wait_for_page_load()
                return True