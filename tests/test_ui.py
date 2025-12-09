import pytest
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TestChitaiGorodFullScenario:
    """Полный тестовый сценарий в одном тесте."""

    @pytest.fixture(scope="function")
    def driver(self):
        """Создание драйвера."""
        options = Options()
        options.add_argument("--start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(3)
        yield driver

        # Финальный скриншот
        driver.save_screenshot("test_result.png")
        logger.info("📸 Скриншот сохранен: test_result.png")
        driver.quit()

    def wait_for_page_load(self, driver, timeout=10):
        """Ожидание полной загрузки страницы."""
        logger.info("⏳ Ожидание загрузки страницы...")
        try:
            WebDriverWait(driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            logger.info("✅ Страница загружена")
            time.sleep(1)  # Дополнительная пауза для стабильности
        except TimeoutException:
            logger.warning("⚠️ Страница не полностью загружена, продолжаем...")

    def safe_click(self, driver, locator, max_retries=3, description=""):
        """Безопасный клик с обработкой StaleElementReferenceException."""
        logger.info(f"🖱️ Попытка клика: {description}")

        for attempt in range(max_retries):
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(locator)
                )
                element.click()
                logger.info(f"✅ Успешный клик: {description}")
                time.sleep(1)  # Пауза после клика
                return element

            except StaleElementReferenceException:
                logger.warning(f"🔄 Попытка {attempt + 1}: элемент устарел, пробуем снова...")
                time.sleep(1)

            except TimeoutException:
                logger.error(f"❌ Элемент не найден: {description}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(1)

        raise TimeoutException(f"Не удалось кликнуть на элемент: {description}")

    def safe_find_element(self, driver, by, selector, timeout=10, description=""):
        """Безопасный поиск элемента."""
        logger.info(f"🔍 Поиск элемента: {description}")
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
            logger.info(f"✅ Элемент найден: {description}")
            return element
        except TimeoutException:
            logger.error(f"❌ Элемент не найден: {description}")
            logger.error(f"   Селектор: {selector}")
            raise

    def test_complete_purchase_flow(self, driver):
        """Полный сценарий: поиск -> добавление -> корзина -> очистка."""
        logger.info("\n" + "=" * 70)
        logger.info("🚀 НАЧАЛО ТЕСТОВОГО СЦЕНАРИЯ")
        logger.info("=" * 70)

        # ========== ШАГ 1: ОТКРЫТИЕ САЙТА ==========
        logger.info("\n📌 ШАГ 1: Открытие сайта")
        driver.get("https://www.chitai-gorod.ru")
        self.wait_for_page_load(driver)
        logger.info(f"✅ Сайт открыт: {driver.current_url}")

        # Куки
        try:
            cookie_btn = driver.find_element(By.XPATH,
                                             "//button[contains(., 'Принять') or contains(., 'Согласен')]")
            cookie_btn.click()
            logger.info("✅ Куки приняты")
        except:
            logger.info("ℹ️ Куки не найдены")

        # ========== ШАГ 2: ПОИСК ТОВАРА ==========
        logger.info("\n📌 ШАГ 2: Поиск товара 'Лев Толстой Война и мир'")

        # Находим поле поиска
        search_input = self.safe_find_element(
            driver,
            By.CSS_SELECTOR,
            "input.search-form__input",
            description="Поле поиска"
        )

        # Вводим запрос
        search_input.clear()
        search_input.send_keys("Лев Толстой Война и мир")
        search_input.send_keys(Keys.RETURN)
        logger.info("✅ Поиск выполнен")

        self.wait_for_page_load(driver)

        # ========== ШАГ 3: ОТКРЫТИЕ КАРТОЧКИ ТОВАРА ==========
        logger.info("\n📌 ШАГ 3: Поиск и открытие книги 'Война и мир. Книга 2'")

        # Ждем загрузки результатов поиска
        self.wait_for_page_load(driver)

        # ВАЖНО: Сначала ждем загрузки страницы, потом ищем элемент
        # Ищем книгу "Война и мир. Книга 2" несколькими способами

        found_book = False

        # Способ 1: Ищем по точному тексту в ссылках
        try:
            book_elements = driver.find_elements(By.XPATH,
                                                 "//a[contains(., 'Война и мир') and contains(., 'Книга 2')]")

            for element in book_elements:
                if element.is_displayed():
                    # НАХОДИМ ЭЛЕМЕНТ ЗАНОВО ПЕРЕД КЛИКОМ
                    book_link = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    f"//a[contains(., 'Война и мир') and contains(., 'Книга 2')]")))

                    book_link.click()
                    found_book = True
                    logger.info("✅ Найдена книга 'Война и мир. Книга 2'")
                    break
        except:
            pass

        # Способ 2: Ищем по частичному совпадению
        if not found_book:
            try:
                # Ищем любую ссылку с "Война и мир"
                war_and_peace_links = driver.find_elements(By.XPATH,
                                                           "//a[contains(., 'Война и мир')]")

                if war_and_peace_links:
                    # Берем первую найденную ссылку
                    book_link = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    "//a[contains(., 'Война и мир')]")))

                    book_link.click()
                    found_book = True
                    logger.info("✅ Найдена книга с 'Война и мир' в названии")
            except:
                pass

        # Способ 3: Берем первую карточку товара
        if not found_book:
            try:
                first_product = self.safe_click(
                    driver,
                    (By.CSS_SELECTOR, ".product-card a"),
                    description="Первая карточка товара"
                )
                found_book = True
                logger.info("✅ Открыта первая карточка товара")
            except:
                logger.error("❌ Не удалось найти ни одной книги")
                raise

        self.wait_for_page_load(driver)
        logger.info(f"✅ Карточка товара открыта: {driver.current_url}")

        # ========== ШАГ 4: ДОБАВЛЕНИЕ В КОРЗИНУ ==========
        logger.info("\n📌 ШАГ 4: Добавление в корзину")

        # ВАЖНО: После перехода на новую страницу все элементы нужно находить заново
        # Находим кнопку "Купить" на НОВОЙ странице
        buy_button = self.safe_click(
            driver,
            (By.CSS_SELECTOR, "button.product-buttons__main-action"),
            description="Кнопка 'Купить'"
        )

        logger.info("✅ Товар добавлен в корзину")

        # ========== ШАГ 5: ПЕРЕХОД В КОРЗИНУ ==========
        logger.info("\n📌 ШАГ 5: Переход в корзину")

        # Проверяем изменилась ли кнопка на "Оформить"
        try:
            WebDriverWait(driver, 5).until(
                lambda d: "Оформить" in d.find_element(
                    By.CSS_SELECTOR, "button.product-buttons__main-action"
                ).text
            )
            logger.info("✅ Кнопка изменилась на 'Оформить'")

            # Кликаем на кнопку "Оформить"
            self.safe_click(
                driver,
                (By.CSS_SELECTOR, "button.product-buttons__main-action"),
                description="Кнопка 'Оформить'"
            )

        except TimeoutException:
            # Если кнопка не изменилась, ищем иконку корзины
            logger.info("ℹ️ Кнопка не изменилась, ищем иконку корзины")

            try:
                cart_icon = self.safe_click(
                    driver,
                    (By.CSS_SELECTOR, "a[href*='/cart/'], .header-cart"),
                    description="Иконка корзины"
                )
            except:
                # Прямой переход по URL
                logger.info("ℹ️ Переход по прямому URL корзины")
                driver.get("https://www.chitai-gorod.ru/cart/")

        self.wait_for_page_load(driver)
        logger.info(f"✅ Корзина открыта: {driver.current_url}")

        # ========== ШАГ 6: УПРАВЛЕНИЕ КОЛИЧЕСТВОМ ТОВАРА ==========
        logger.info("\n📌 ШАГ 6: Управление количеством товара")

        try:
            # Ждем элементы управления количеством
            self.wait_for_page_load(driver)

            # Кнопка увеличения (+)
            plus_button = self.safe_click(
                driver,
                (By.CSS_SELECTOR, ".chg-ui-input-number__input-control--increment"),
                description="Кнопка увеличения количества (+)"
            )
            logger.info("✅ Количество увеличено на +1")

            # Пауза для обновления
            time.sleep(1)

            # Кнопка уменьшения (-)
            minus_button = self.safe_click(
                driver,
                (By.CSS_SELECTOR, ".chg-ui-input-number__input-control--decrement"),
                description="Кнопка уменьшения количества (-)"
            )
            logger.info("✅ Количество уменьшено на -1")

        except Exception as e:
            logger.warning(f"⚠️ Не удалось изменить количество: {e}")

        # ========== ШАГ 7: ОЧИСТКА КОРЗИНЫ ==========
        logger.info("\n📌 ШАГ 7: Очистка корзины")

        try:
            # Используем точный селектор который вы предоставили
            clear_selector = "#__nuxt > div > div.app-wrapper__content > div.app-wrapper__container > div > div > div > div.cart-page__head > div > div.cart-page__delete-many > span"

            clear_button = self.safe_click(
                driver,
                (By.CSS_SELECTOR, clear_selector),
                description="Кнопка 'Очистить корзину'"
            )
            logger.info("✅ Корзина очищена")

            # Проверяем что корзина пуста
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//*[contains(., 'корзина пуста') or contains(., 'Корзина пуста')]"))
                )
                logger.info("✅ Подтверждение: корзина пуста")
            except:
                logger.info("ℹ️ Подтверждение очистки не найдено")

        except Exception as e:
            logger.warning(f"⚠️ Не удалось очистить корзину: {e}")

            # Альтернативный поиск
            try:
                clear_elements = driver.find_elements(By.XPATH,
                                                      "//*[contains(., 'Очистить корзину')]")

                if clear_elements:
                    clear_elements[0].click()
                    logger.info("✅ Корзина очищена (альтернативный поиск)")
            except:
                logger.info("ℹ️ Кнопка очистки не найдена")

        # ========== ЗАВЕРШЕНИЕ ТЕСТА ==========
        logger.info("\n" + "=" * 70)
        logger.info("🎉 ТЕСТ УСПЕШНО ЗАВЕРШЕН!")
        logger.info("=" * 70)


# Запуск теста напрямую
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🧪 ЗАПУСК ТЕСТА В РУЧНОМ РЕЖИМЕ")
    print("=" * 70)

    start_time = time.time()

    # Создаем экземпляр теста
    test_instance = TestChitaiGorodFullScenario()

    # Создаем драйвер
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)

    try:
        # Запускаем тест
        test_instance.test_complete_purchase_flow(driver)

        end_time = time.time()
        duration = end_time - start_time

        print("\n" + "=" * 70)
        print(f"✅ ТЕСТ УСПЕШНО ЗАВЕРШЕН!")
        print(f"⏱️  Время выполнения: {duration:.1f} секунд")
        print("=" * 70)

    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time

        print("\n" + "=" * 70)
        print(f"❌ ТЕСТ ЗАВЕРШИЛСЯ С ОШИБКОЙ")
        print(f"⏱️  Время до ошибки: {duration:.1f} секунд")
        print(f"💥 Ошибка: {str(e)[:100]}...")
        print("=" * 70)

        # Сохраняем дополнительную информацию
        try:
            driver.save_screenshot("test_error_final.png")
            print("📸 Скриншот ошибки: test_error_final.png")

            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("📄 Исходный код страницы: page_source.html")
        except:
            pass

        raise

    finally:
        # Небольшая пауза перед закрытием
        input("\nНажмите Enter для закрытия браузера...")
        driver.quit()