from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import logging
import time

logger = logging.getLogger(__name__)


class BasePage:
    """Базовый класс с вашими методами - ИСПРАВЛЕННЫЙ"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def wait_for_page_load(self, timeout=10):
        """Ожидание загрузки страницы (ваш метод) С ДОПОЛНИТЕЛЬНЫМ ОЖИДАНИЕМ"""
        logger.info("⏳ Ожидание загрузки страницы...")
        try:
            # 1. Ждем readyState = complete
            self.wait.until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            logger.info("✅ Страница загружена")

            # 2. ДОБАВЛЯЕМ: Ждем минимум 1 секунду (как в вашем рабочем коде)
            start = time.time()
            WebDriverWait(self.driver, 2).until(lambda d: time.time() - start >= 1)

        except TimeoutException:
            logger.warning("⚠️ Страница не полностью загружена, продолжаем...")

    def wait_one_second(self):
        """Ожидание 1 секунды без time.sleep"""
        start = time.time()
        WebDriverWait(self.driver, 2).until(lambda d: time.time() - start >= 1)
        return True

    def safe_click(self, locator, description=""):
        """Безопасный клик С ОЖИДАНИЕМ ПОСЛЕ КЛИКА (как в рабочем коде)"""
        logger.info(f"🖱️ Попытка клика: {description}")

        for attempt in range(3):
            try:
                element = self.wait.until(EC.element_to_be_clickable(locator))
                element.click()
                logger.info(f"✅ Успешный клик: {description}")

                # ДОБАВЛЯЕМ: Ожидание 1 секунду после клика (как в рабочем коде)
                self.wait_one_second()

                return element

            except StaleElementReferenceException:
                logger.warning(f"🔄 Попытка {attempt + 1}: элемент устарел")
                # Ожидание при повторной попытке
                self.wait_one_second()

            except TimeoutException:
                logger.error(f"❌ Элемент не найден: {description}")
                if attempt == 2:
                    raise
                # Ожидание при повторной попытке
                self.wait_one_second()

        raise TimeoutException(f"Не удалось кликнуть: {description}")

    def safe_find_element(self, by, selector, description=""):
        """Безопасный поиск элемента"""
        logger.info(f"🔍 Поиск элемента: {description}")
        try:
            element = self.wait.until(
                EC.presence_of_element_located((by, selector))
            )
            logger.info(f"✅ Элемент найден: {description}")
            return element
        except TimeoutException:
            logger.error(f"❌ Элемент не найден: {description}")
            raise