from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage  # <-- ТОЧКА перед base_page!
import allure
import logging
import time

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    """Страница корзины с вашим таймингом"""

    # Локаторы
    PLUS_BUTTON = (By.CSS_SELECTOR, ".chg-ui-input-number__input-control--increment")
    MINUS_BUTTON = (By.CSS_SELECTOR, ".chg-ui-input-number__input-control--decrement")
    CLEAR_BUTTON = (By.CSS_SELECTOR, "#__nuxt > div > div.app-wrapper__content > div.app-wrapper__container > div > div > div > div.cart-page__head > div > div.cart-page__delete-many > span")

    def increase_quantity(self):
        """Увеличение количества - ТОЧНО как в рабочем коде"""
        logger.info("➕ Увеличение количества")

        try:
            # 1. Ждем элементы управления количеством
            self.wait_for_page_load()

            # 2. Кнопка увеличения (+)
            plus_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".chg-ui-input-number__input-control--increment")
                )
            )

            # 3. Кликаем
            plus_button.click()
            logger.info("✅ Количество увеличено на +1")

            # 4. Ждем обновления - ВАЖНО!
            start = time.time()
            WebDriverWait(self.driver, 2).until(lambda d: time.time() - start >= 1)

            return True
        except Exception as e:
            logger.warning(f"⚠️ Не удалось увеличить количество: {e}")
            return False

    def decrease_quantity(self):
        """Уменьшение количества - ТОЧНО как в рабочем коде"""
        logger.info("➖ Уменьшение количества")

        try:
            # 1. Ждем элементы управления количеством
            self.wait_for_page_load()

            # 2. Кнопка уменьшения (-)
            minus_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".chg-ui-input-number__input-control--decrement")
                )
            )

            # 3. Кликаем
            minus_button.click()
            logger.info("✅ Количество уменьшено на -1")

            return True
        except Exception as e:
            logger.warning(f"⚠️ Не удалось уменьшить количество: {e}")
            return False

    def clear_cart(self):
        """Очистка корзины - ТОЧНО как в рабочем коде"""
        logger.info("🗑️ Очистка корзины")

        try:
            # ТОЧНЫЙ СЕЛЕКТОР из рабочего кода
            clear_selector = "#__nuxt > div > div.app-wrapper__content > div.app-wrapper__container > div > div > div > div.cart-page__head > div > div.cart-page__delete-many > span"

            # Используем safe_click
            self.safe_click(
                (By.CSS_SELECTOR, clear_selector),
                description="Кнопка 'Очистить корзину'"
            )
            logger.info("✅ Корзина очищена")

            # Проверяем что корзина пуста
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        "//*[contains(., 'корзина пуста') or contains(., 'Корзина пуста')]"
                    ))
                )
                logger.info("✅ Подтверждение: корзина пуста")
            except:
                logger.info("ℹ️ Подтверждение очистки не найдено")

            return True
        except Exception as e:
            logger.warning(f"⚠️ Не удалось очистить корзину: {e}")

            # Альтернативный поиск (как в рабочем коде)
            try:
                clear_elements = self.driver.find_elements(
                    By.XPATH,
                    "//*[contains(., 'Очистить корзину')]"
                )

                if clear_elements:
                    clear_elements[0].click()
                    logger.info("✅ Корзина очищена (альтернативный поиск)")
                    return True
            except:
                logger.info("ℹ️ Кнопка очистки не найдена")

            return False