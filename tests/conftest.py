"""Конфигурация pytest."""
import pytest
import allure
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания отчетов Allure."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # Получаем драйвер из фикстуры
        for fixture_name in item.fixturenames:
            if "driver" in fixture_name:
                try:
                    driver = item.funcargs[fixture_name]
                    if hasattr(driver, 'get_screenshot_as_png'):
                        # Прикрепляем скриншот к Allure
                        allure.attach(
                            driver.get_screenshot_as_png(),
                            name="screenshot_on_failure",
                            attachment_type=allure.attachment_type.PNG
                        )

                        # Прикрепляем исходный код страницы
                        allure.attach(
                            driver.page_source,
                            name="page_source_on_failure",
                            attachment_type=allure.attachment_type.TEXT
                        )

                        # Прикрепляем текущий URL
                        allure.attach(
                            driver.current_url,
                            name="url_on_failure",
                            attachment_type=allure.attachment_type.TEXT
                        )
                except Exception as e:
                    logging.error(f"Не удалось прикрепить данные к Allure: {e}")
                break


@pytest.fixture(scope="function")
def driver():
    """Фикстура создания драйвера."""
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)

    yield driver

    # Финальные действия
    try:
        driver.save_screenshot("test_result.png")
        logging.info("📸 Скриншот сохранен: test_result.png")
    except Exception as e:
        logging.error(f"❌ Не удалось сохранить скриншот: {e}")
    finally:
        driver.quit()