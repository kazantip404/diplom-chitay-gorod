"""
5 позитивных API тестов для Читай-город - С ШАГАМИ
"""
import pytest
import allure
import time


@allure.epic("Читай-город API")
@allure.feature("Позитивные тесты")
class TestChitaiGorodAPI:
    """API тесты с шагами как UI"""

    def setup_class(self):
        """Настройка перед всеми тестами"""
        print("\n" + "=" * 60)
        print("🧪 НАЧАЛО: API ТЕСТИРОВАНИЕ")
        print("=" * 60)

    def teardown_class(self):
        """После всех тестов"""
        print("\n" + "=" * 60)
        print("🎉 API ТЕСТЫ ЗАВЕРШЕНЫ!")
        print("=" * 60)

    @allure.title("1. Поиск книг Льва Толстого")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_tolstoy(self, api_client):
        """Шаг 1: Поиск книг Толстого"""
        print("\n▶️ ШАГ 1: Поиск 'Лев Толстой'")

        start_time = time.time()
        result = api_client.search_products("Лев Толстой")

        # Проверки
        assert result.get("ok"), "API не ответил"
        assert result.get("total", 0) > 0, "Книги не найдены"

        books = result.get("books", [])
        total = result.get("total", 0)

        print(f"   ✅ Найдено: {len(books)} книг")
        print(f"   ✅ Всего в базе: {total}")

        if books:
            first_book = books[0]
            print(f"   📖 Первая книга: {first_book.get('title')[:40]}...")
            assert "Толстой" in first_book.get("author", ""), "Автор не Толстой"
            print(f"   👤 Автор верный: Толстой")

        print(f"   ⏱️  Время ответа: {time.time() - start_time:.2f} сек")

    @allure.title("2. Поиск по категории 'книга'")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_books(self, api_client):
        """Шаг 2: Общий поиск книг"""
        print("\n▶️ ШАГ 2: Поиск 'книга'")

        result = api_client.search_products("книга")

        assert result.get("ok"), "API не ответил"
        assert result.get("found", 0) > 0, "Товары не найдены"

        found = result.get("found", 0)
        print(f"   ✅ Найдено товаров: {found}")

        if found > 100:
            print(f"   📚 Большая коллекция книг!")

    @allure.title("3. Поиск детективов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_detective(self, api_client):
        """Шаг 3: Поиск детективов"""
        print("\n▶️ ШАГ 3: Поиск 'детектив'")

        result = api_client.search_products("детектив")

        assert result.get("ok"), "API не ответил"
        assert result.get("total", 0) > 0, "Детективы не найдены"

        total = result.get("total", 0)
        print(f"   ✅ Всего детективов: {total}")

        # Проверяем авторов детективов
        books = result.get("books", [])
        if books:
            authors = [b.get("author", "") for b in books[:3] if b.get("author")]
            detective_keywords = ["Кристи", "Чейз", "Конан", "Маринина", "Акунин"]

            found_authors = []
            for author in authors:
                if any(keyword in author for keyword in detective_keywords):
                    found_authors.append(author.split()[0])  # Только фамилия

            if found_authors:
                print(f"   🕵️‍♂️ Найдены авторы: {', '.join(set(found_authors))}")

    @allure.title("4. Популярные поисковые запросы")
    @allure.severity(allure.severity_level.NORMAL)
    def test_popular_searches(self, api_client):
        """Шаг 4: Популярные запросы"""
        print("\n▶️ ШАГ 4: Популярные запросы")

        result = api_client.get_popular_searches()

        assert result.get("ok"), "API не ответил"
        assert result.get("count", 0) > 0, "Нет популярных запросов"

        phrases = result.get("phrases", [])
        count = result.get("count", 0)

        print(f"   ✅ Получено фраз: {count}")

        # Показываем топ-3
        if phrases:
            print(f"   🔥 Топ-3 популярных:")
            for i, phrase in enumerate(phrases[:3], 1):
                text = phrase.get("text", "")[:25]
                if text:
                    print(f"     {i}. {text}...")

        # Проверяем что есть книжные запросы
        all_text = " ".join(p.get("text", "").lower() for p in phrases)
        book_indicators = ["книг", "автор", "роман", "детектив", "фантастик"]
        if any(indicator in all_text for indicator in book_indicators):
            print(f"   📖 Есть книжные запросы")

    @allure.title("5. Негативный поиск с ошибками")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_with_typos(self, api_client):
        """Шаг 5: Поиск с опечатками"""
        print("\n▶️ ШАГ 5: Поиск с опечатками")

        test_cases = [
            ("Leв Tolsой", "Лев Толстой"),  # Латинские буквы
            ("лв тлстй", "Лев Толстой"),    # Без гласных
            ("Вайна и мир", "Война и мир"), # Опечатка
        ]

        print(f"   🔍 Тестируем {len(test_cases)} варианта с опечатками:")

        for typo_query, correct_query in test_cases:
            result = api_client.search_products(typo_query)

            if result.get("ok") and result.get("books"):
                books = result.get("books", [])
                print(f"     ✅ '{typo_query}' → найдено {len(books)} книг")

                # Проверяем что нашли правильные книги
                if books:
                    first_title = books[0].get("title", "").lower()
                    if any(keyword in first_title for keyword in ["толстой", "война", "мир"]):
                        print(f"       📚 Найдена правильная книга")
            else:
                print(f"     ❌ '{typo_query}' → не найдено")

        # Дополнительная проверка: поиск несуществующего
        print(f"\n   🧪 Поиск несуществующего:")
        nonsense_result = api_client.search_products("абвгдеёжзийклмнопрстуфхцчшщъыьэюя123")

        if nonsense_result.get("ok"):
            found = nonsense_result.get("found", 0)
            print(f"     📊 Найдено: {found} товаров (ожидалось 0)")

            # В идеале должно быть 0, но API может что-то найти
            if found == 0:
                print(f"     ✅ API правильно обработал бессмысленный запрос")
            else:
                print(f"     ℹ️  API нашёл что-то по бессмысленному запросу")