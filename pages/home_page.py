"""Главная страница."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import TestConfig


class HomePage(BasePage):
    """Главная страница сайта."""

    def __init__(self, driver):
        super().__init__(driver)

    def open(self) -> None:
        """Открытие главной страницы."""
        self.driver.get(TestConfig.BASE_URL)
        self.wait_for_page_load()

    def accept_cookies(self) -> bool:
        """Принятие cookies."""
        try:
            cookie_btn = self.driver.find_element(
                By.XPATH,
                TestConfig.Selectors.COOKIE_BUTTON
            )
            cookie_btn.click()
            self.logger.info("✅ Куки приняты")
            self.wait_utils.wait_exact(1)
            return True
        except Exception:
            self.logger.info("ℹ️ Куки не найдены или уже приняты")
            return False