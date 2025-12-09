"""Базовый класс для всех страниц."""
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from config.config import TestConfig
from utils.wait_utils import WaitUtils


class BasePage:
    """Базовый класс страницы."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait_utils = WaitUtils(driver)
        self.logger = logging.getLogger(__name__)

    def wait_for_page_load(self, timeout: int = TestConfig.TIMEOUT) -> None:
        """Ожидание загрузки страницы."""
        self.logger.info("⏳ Ожидание загрузки страницы...")
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            self.logger.info("✅ Страница загружена")
            self.wait_utils.wait_exact(1)
        except TimeoutException:
            self.logger.warning("⚠️ Страница не полностью загружена, продолжаем...")

    def safe_click(self, locator: tuple, max_retries: int = 3, description: str = ""):
        """Безопасный клик с обработкой StaleElementReferenceException."""
        self.logger.info(f"🖱️ Попытка клика: {description}")

        for attempt in range(max_retries):
            try:
                element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(locator)
                )
                element.click()
                self.logger.info(f"✅ Успешный клик: {description}")
                self.wait_utils.wait_exact(1)
                return element

            except StaleElementReferenceException:
                self.logger.warning(f"🔄 Попытка {attempt + 1}: элемент устарел, пробуем снова...")
                self.wait_utils.wait_exact(1)

            except TimeoutException:
                self.logger.error(f"❌ Элемент не найден: {description}")
                if attempt == max_retries - 1:
                    raise
                self.wait_utils.wait_exact(1)

        raise TimeoutException(f"Не удалось кликнуть на элемент: {description}")

    def safe_find_element(self, by: By, selector: str, timeout: int = TestConfig.TIMEOUT, description: str = ""):
        """Безопасный поиск элемента."""
        self.logger.info(f"🔍 Поиск элемента: {description}")
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
            self.logger.info(f"✅ Элемент найден: {description}")
            return element
        except TimeoutException:
            self.logger.error(f"❌ Элемент не найден: {description}")
            self.logger.error(f"   Селектор: {selector}")
            raise