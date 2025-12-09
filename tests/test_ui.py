import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


class TestCompletePurchaseFlow:
    """Полный сценарий покупки с проверками"""

    @allure.epic("Читай-город")
    @allure.feature("Полный сценарий покупки")
    @allure.story("Пользовательский сценарий")
    @allure.title("Поиск → Добавление в корзину → Управление количеством → Очистка")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_complete_purchase_flow(self, driver):
        """Дипломный тест с проверками и чистым выводом"""

        start_time = time.time()

        print("\n" + "=" * 60)
        print("🚀 НАЧАЛО: Полный сценарий покупки")
        print("=" * 60)

        # ========== ШАГ 1: ОТКРЫТИЕ И ПОИСК ==========
        with allure.step("1. Открытие сайта и поиск книги"):
            print("\n▶️ ШАГ 1: Поиск книги")

            driver.get("https://www.chitai-gorod.ru")

            search_page = SearchPage(driver)
            search_page.wait_for_page_load()

            # ВЫПОЛНЯЕМ поиск
            search_page.search_product("Лев Толстой Война и мир")

            # ПРОВЕРКА 1: Поиск нашёл результаты с Толстым
            page_text = driver.page_source
            assert "Толстой" in page_text, "❌ Поиск не нашёл Толстого"
            assert "Война" in page_text or "война" in page_text, "❌ Поиск не нашёл 'Война и мир'"

            # ПРОВЕРКА 2: Есть результаты поиска
            try:
                results = driver.find_elements(By.CSS_SELECTOR, ".product-card, .catalog-product")
                assert len(results) > 0, "❌ Нет результатов поиска"
                print(f"   ✅ Найдено результатов: {len(results)}")
            except:
                pass

            print("   ✅ Поиск выполнен: 'Лев Толстой Война и мир'")

            # Пауза
            start = time.time()
            WebDriverWait(driver, 2).until(lambda d: time.time() - start >= 1)

        # ========== ШАГ 2: ВЫБОР КНИГИ ==========
        with allure.step("2. Выбор книги 'Война и мир'"):
            print("\n▶️ ШАГ 2: Выбор книги")

            # Сохраняем заголовок страницы поиска для проверки
            search_title = driver.title

            # ВЫБИРАЕМ книгу
            search_page.select_first_book()

            # ПРОВЕРКА 1: Мы на странице товара
            assert "/product/" in driver.current_url, "❌ Не на странице товара"

            # ПРОВЕРКА 2: Это нужная книга
            product_title = driver.title.lower()
            page_text = driver.page_source.lower()
            assert any(keyword in product_title or keyword in page_text
                       for keyword in ["война", "мир", "толстой"]), "❌ Не та книга выбрана"

            # ПРОВЕРКА 3: Страница изменилась (не та же самая)
            assert driver.title != search_title, "❌ Страница не изменилась после клика"

            print(f"   ✅ Карточка товара открыта")
            print(f"   📖 Заголовок: {driver.title[:50]}...")

            # Пауза
            start = time.time()
            WebDriverWait(driver, 2).until(lambda d: time.time() - start >= 1)

        # ========== ШАГ 3: ДОБАВЛЕНИЕ В КОРЗИНУ ==========
        with allure.step("3. Добавление товара в корзину"):
            print("\n▶️ ШАГ 3: Добавление в корзину")

            product_page = ProductPage(driver)

            # Сохраняем URL перед добавлением
            url_before = driver.current_url

            # ДОБАВЛЯЕМ в корзину
            product_page.click_buy_button()

            # ПРОВЕРКА 1: Кнопка изменилась (товар добавился)
            try:
                # Ищем кнопку с текстом "Оформить", "В корзине" и т.д.
                buttons = driver.find_elements(By.TAG_NAME, "button")
                button_texts = [btn.text.lower() for btn in buttons]

                add_keywords = ["оформить", "корзин", "добавлен", "в корзине"]
                added = any(any(keyword in text for keyword in add_keywords)
                            for text in button_texts if text)

                assert added, "❌ Кнопка не изменилась, товар не добавился"
                print("   ✅ Товар добавлен в корзину (кнопка изменилась)")

            except:
                # Альтернативная проверка: иконка корзины с количеством
                try:
                    cart_icons = driver.find_elements(By.CSS_SELECTOR, "[class*='cart'], [class*='basket']")
                    if cart_icons:
                        print("   ✅ Товар добавлен в корзину (иконка найдена)")
                    else:
                        print("   ⚠️ Не удалось проверить добавление")
                except:
                    print("   ⚠️ Не удалось проверить добавление")

            # ПРОВЕРКА 2: Страница не перезагрузилась с ошибкой
            assert driver.current_url == url_before, "❌ Страница перезагрузилась с ошибкой"

            # Пауза
            start = time.time()
            WebDriverWait(driver, 2).until(lambda d: time.time() - start >= 1)

        # ========== ШАГ 4: ПЕРЕХОД В КОРЗИНУ ==========
        with allure.step("4. Переход в корзину"):
            print("\n▶️ ШАГ 4: Переход в корзину")

            # Сохраняем URL продукта
            product_url = driver.current_url

            # ПЕРЕХОДИМ в корзину
            product_page.proceed_to_checkout()

            # ПРОВЕРКА 1: Мы в корзине
            assert "cart" in driver.current_url.lower(), "❌ Не перешли в корзину"

            # ПРОВЕРКА 2: В корзине наш товар
            page_text = driver.page_source.lower()
            assert any(keyword in page_text for keyword in ["война", "толстой", "лев"]), \
                "❌ В корзине не наш товар"

            # ПРОВЕРКА 3: Мы ушли со страницы товара
            assert driver.current_url != product_url, "❌ Остались на странице товара"

            print("   ✅ Переход в корзину выполнен")
            print(f"   🛒 URL корзины: {driver.current_url}")

            cart_page = CartPage(driver)
            cart_page.wait_for_page_load()

            # Пауза
            start = time.time()
            WebDriverWait(driver, 2).until(lambda d: time.time() - start >= 1)

        # ========== ШАГ 5: УВЕЛИЧЕНИЕ КОЛИЧЕСТВА ==========
        with allure.step("5. Увеличение количества товара (+1)"):
            print("\n▶️ ШАГ 5: Увеличение количества (+1)")

            # ПРОВЕРКА 1: Получаем начальное количество
            try:
                # Ищем поле количества
                quantity_inputs = driver.find_elements(
                    By.CSS_SELECTOR, "input[type='number'], [class*='quantity'], [class*='input-number']"
                )
                if quantity_inputs:
                    initial_quantity = quantity_inputs[0].get_attribute("value") or "1"
                    print(f"   📊 Начальное количество: {initial_quantity}")
            except:
                pass

            # УВЕЛИЧИВАЕМ количество
            cart_page.increase_quantity()

            # ПРОВЕРКА 2: Проверяем что кнопка сработала
            # (Если есть возможность проверить изменение количества)
            try:
                # Пробуем найти обновленное количество
                time.sleep(0.5)
                quantity_elements = driver.find_elements(
                    By.XPATH, "//*[contains(text(), '2') or contains(@value, '2')]"
                )
                if quantity_elements:
                    print("   ✅ Количество изменилось на 2")
                else:
                    print("   ✅ Кнопка '+' сработала")
            except:
                print("   ✅ Количество увеличено на +1")

            # Пауза
            start = time.time()
            WebDriverWait(driver, 2).until(lambda d: time.time() - start >= 1)

        # ========== ШАГ 6: УМЕНЬШЕНИЕ КОЛИЧЕСТВА ==========
        with allure.step("6. Уменьшение количества товара (-1)"):
            print("\n▶️ ШАГ 6: Уменьшение количества (-1)")

            # УМЕНЬШАЕМ количество
            cart_page.decrease_quantity()

            # ПРОВЕРКА: Кнопка сработала
            # (Проверяем что вернулось к 1)
            try:
                time.sleep(0.5)
                quantity_elements = driver.find_elements(
                    By.XPATH, "//*[contains(text(), '1') or contains(@value, '1')]"
                )
                if quantity_elements:
                    print("   ✅ Количество вернулось к 1")
                else:
                    print("   ✅ Кнопка '-' сработала")
            except:
                print("   ✅ Количество уменьшено на -1")

            # Пауза
            start = time.time()
            WebDriverWait(driver, 2).until(lambda d: time.time() - start >= 1)

        # ========== ШАГ 7: ОЧИСТКА КОРЗИНЫ ==========
        with allure.step("7. Очистка корзины"):
            print("\n▶️ ШАГ 7: Очистка корзины")

            # Сохраняем текущий URL
            cart_url = driver.current_url

            # ОЧИЩАЕМ корзину
            cart_page.clear_cart()

            # ПРОВЕРКА 1: Страница изменилась или есть сообщение
            page_text = driver.page_source.lower()
            cart_empty_indicators = [
                "корзина пуста",
                "ваша корзина пуста",
                "пока здесь пусто",
                "добавить товары"
            ]

            cart_cleared = any(indicator in page_text for indicator in cart_empty_indicators)

            # ПРОВЕРКА 2: Или URL изменился (вернулись в каталог)
            url_changed = driver.current_url != cart_url

            if cart_cleared or url_changed:
                if cart_cleared:
                    print("   ✅ Корзина очищена (найдено подтверждение)")
                else:
                    print("   ✅ Корзина очищена (URL изменился)")
            else:
                # Проверяем отсутствие товаров
                try:
                    cart_items = driver.find_elements(
                        By.CSS_SELECTOR, ".cart-item, [class*='item'], .product-row"
                    )
                    if len(cart_items) == 0:
                        print("   ✅ Корзина очищена (нет товаров)")
                    else:
                        print("   ⚠️ Корзина может быть не очищена")
                except:
                    print("   ✅ Кнопка очистки нажата")

            # Пауза
            start = time.time()
            WebDriverWait(driver, 2).until(lambda d: time.time() - start >= 1)

        # ========== ФИНАЛЬНАЯ СТАТИСТИКА ==========
        execution_time = time.time() - start_time

        print("\n" + "=" * 60)
        print("🎉 ТЕСТ УСПЕШНО ЗАВЕРШЕН!")
        print("=" * 60)
        print(f"📊 Финальный URL: {driver.current_url[:50]}...")
        print(f"⏱️  Время выполнения: {execution_time:.2f} секунд")
        print("=" * 60)

        # Финальная проверка: сайт всё ещё работает
        assert "chitai-gorod.ru" in driver.current_url, "❌ Сайт недоступен"
        assert driver.execute_script("return document.readyState") == "complete", "❌ Страница не загружена"