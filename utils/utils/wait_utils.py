"""Утилиты для ожиданий."""
import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait


class WaitUtils:
    """Утилиты для ожиданий."""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def wait_exact(self, seconds: float) -> None:
        """Точное ожидание указанного количества секунд."""
        start = time.time()
        WebDriverWait(self.driver, seconds + 1).until(
            lambda d: time.time() - start >= seconds
        )