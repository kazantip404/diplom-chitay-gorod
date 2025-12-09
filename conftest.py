import pytest
import logging
import sys
import os
import time

# Добавляем путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Глобальная настройка логирования - МИНИМАЛЬНАЯ
logging.basicConfig(
    level=logging.WARNING,  # По умолчанию только WARNING и ERROR
    format='%(message)s'  # Упрощенный формат
)

# Импорты для обратной совместимости
try:
    from config import Config
except ImportError:
    class Config:
        BASE_URL = "https://www.chitai-gorod.ru"
        API_BASE_URL = "https://web-agr.chitai-gorod.ru"
        TIMEOUT = 15
        DEFAULT_CITY_ID = 213
        TEST_AUTH_TOKEN = ""

# Импортируем API клиент
try:
    from api.base_client import ChitaiGorodAPIClient
except ImportError:
    class ChitaiGorodAPIClient:
        def __init__(self, use_auth=True):
            pass

        def search_products(self, phrase):
            return {"ok": False, "error": "API client not loaded"}

        def get_popular_searches(self):
            return {"ok": False, "error": "API client not loaded"}


# ========== ФИКСТУРЫ ==========
@pytest.fixture(scope="function")
def driver():
    """WebDriver для UI тестов - БЕЗ ЛОГОВ И БЕЗ ОШИБОК CHROME"""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Убирает DevTools лог
    options.add_argument('--log-level=3')  # Уровень логов: 0=INFO, 1=WARNING, 2=ERROR, 3=FATAL
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-blink-features=AutomationControlled')

    # Убираем лишние сообщения в консоль
    options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)

    yield driver

    driver.quit()


@pytest.fixture(scope="function")
def api_client():
    """API клиент С авторизацией - БЕЗ ЛОГОВ"""
    try:
        client = ChitaiGorodAPIClient(use_auth=True)
    except:
        client = ChitaiGorodAPIClient()
    yield client


@pytest.fixture(scope="function")
def api_client_no_auth():
    """API клиент БЕЗ авторизации - БЕЗ ЛОГОВ"""
    try:
        client = ChitaiGorodAPIClient(use_auth=False)
    except:
        client = ChitaiGorodAPIClient()
    yield client


# ========== ХУКИ ДЛЯ РАЗНЫХ ТЕСТОВ ==========
def pytest_runtest_setup(item):
    """Настройка перед каждым тестом"""
    # Для API тестов - ВКЛЮЧАЕМ логи API (но не детальные)
    if "test_api" in item.nodeid:
        api_logger = logging.getLogger('api')
        api_logger.setLevel(logging.INFO)  # INFO для API

        # Убираем логи HTTP запросов (детальные)
        requests_logger = logging.getLogger('urllib3')
        requests_logger.setLevel(logging.WARNING)

    # Для UI тестов - ВЫКЛЮЧАЕМ ВСЕ ЛОГИ
    elif "test_ui" in item.nodeid:
        # Выключаем все логи для UI тестов
        for logger_name in ['pages', 'selenium', 'urllib3']:
            logging.getLogger(logger_name).setLevel(logging.WARNING)


def pytest_sessionstart(session):
    """Вывод в начале тестовой сессии"""
    session.config.start_time = time.time()
    print("\n" + "=" * 70)
    print("🧪 ЗАПУСК АВТОМАТИЗИРОВАННОГО ТЕСТИРОВАНИЯ")
    print("=" * 70)
    print("Проект: Читай-город")
    print("Тесты: UI + API")
    print("=" * 70)


def pytest_runtest_logstart(nodeid, location):
    """Вывод при начале каждого теста"""
    test_name = nodeid.split("::")[-1]
    test_type = "API" if "test_api" in nodeid else "UI"
    print(f"\n▶️ ЗАПУСК {test_type} ТЕСТА: {test_name}")


def pytest_sessionfinish(session, exitstatus):
    """Вывод в конце тестовой сессии"""
    print("\n" + "=" * 70)

    if exitstatus == 0:
        print("🎉 ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ!")
    else:
        print("❌ ЕСТЬ ПРОБЛЕМЫ В ТЕСТАХ")

    # Статистика
    stats = getattr(session.config, 'stats', {})
    passed = len(stats.get('passed', []))
    failed = len(stats.get('failed', []))
    skipped = len(stats.get('skipped', []))

    print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
    print(f"   ✅ Успешно: {passed}")
    print(f"   ❌ Провалено: {failed}")
    print(f"   ⏭️  Пропущено: {skipped}")
    print(f"   📊 Всего тестов: {passed + failed + skipped}")

    # Время выполнения
    if hasattr(session.config, 'start_time'):
        duration = time.time() - session.config.start_time
        print(f"   ⏱️  Время выполнения: {duration:.2f} секунд")

    print("=" * 70)


# Хук для сбора статистики
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Собираем статистику по тестам"""
    outcome = yield
    report = outcome.get_result()

    # Инициализируем статистику если её нет
    if not hasattr(item.config, 'stats'):
        item.config.stats = {'passed': [], 'failed': [], 'skipped': []}

    # Добавляем тест в соответствующую категорию
    if report.when == 'call':  # Только завершенные тесты
        if report.passed:
            item.config.stats['passed'].append(item.nodeid)
        elif report.failed:
            item.config.stats['failed'].append(item.nodeid)
        elif report.skipped:
            item.config.stats['skipped'].append(item.nodeid)