import requests
import json
import time
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


class TokenManager:
    """🔐 МЕНЕДЖЕР ТОКЕНОВ - автоматическое получение и обновление токенов"""

    def __init__(self):
        self.token_file = "token_cache.json"
        self.base_url = "https://www.chitai-gorod.ru"
        self.api_url = "https://web-agr.chitai-gorod.ru/web/api"

    def get_cached_token(self):
        """📂 Получить токен из кэша (если он еще валидный)"""
        try:
            if os.path.exists(self.token_file):
                with open(self.token_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)

                # 🔍 Проверяем не истек ли токен
                expires_at = datetime.fromisoformat(cache['expires_at'])
                if datetime.now() < expires_at:
                    print("✅ Используем токен из кэша")
                    return cache['access_token']
                else:
                    print("🕒 Токен в кэше истек")

        except Exception as e:
            print(f"⚠️ Ошибка чтения кэша: {e}")

        return None

    def save_token_to_cache(self, access_token, expires_in=86400):
        """💾 Сохранить токен в кэш"""
        try:
            expires_at = datetime.now() + timedelta(seconds=expires_in - 300)  # -5 минут для запаса

            cache_data = {
                'access_token': access_token,
                'expires_at': expires_at.isoformat(),
                'cached_at': datetime.now().isoformat()
            }

            with open(self.token_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)

            print("💾 Токен сохранен в кэш")

        except Exception as e:
            print(f"⚠️ Ошибка сохранения кэша: {e}")

    def get_token_from_browser_storage(self):
        """🖥️ Получить токен через Selenium (имитация браузера)"""
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service as ChromeService
            from selenium.webdriver.chrome.options import Options

            print("🖥️ Запуск браузера для получения токена...")

            # ⚙️ Настройки Chrome
            options = Options()
            options.add_argument("--headless")  # 🖥️ Без графического интерфейса
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

            # 🚀 Запуск браузера
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )

            try:
                # 🔐 Переходим на страницу авторизации
                driver.get(f"{self.base_url}/auth")

                # ⏳ Ждем загрузки
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                # 🔍 Получаем токен из Local Storage
                token_script = """
                var token = localStorage.getItem('access-token');
                if (!token) {
                    token = localStorage.getItem('authorization');
                }
                return token || '';
                """

                token = driver.execute_script(token_script)

                if token:
                    print("✅ Токен получен из браузера")
                    # 🧹 Очищаем токен от лишних символов
                    token = token.replace("Bearer%20", "Bearer ")
                    return token
                else:
                    print("❌ Токен не найден в Local Storage")
                    return None

            finally:
                driver.quit()

        except Exception as e:
            print(f"❌ Ошибка получения токена через браузер: {e}")
            return None

    def get_token_via_api(self, email, password):
        """🔑 Получить токен через API авторизацию"""
        try:
            # 🎯 URL для авторизации (может потребоваться найти правильный endpoint)
            auth_url = f"{self.api_url}/v1/auth/login"

            payload = {
                "email": email,
                "password": password
            }

            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            response = requests.post(auth_url, json=payload, headers=headers, timeout=30)

            if response.status_code == 200:
                data = response.json()
                token = data.get('access_token')
                if token:
                    print("✅ Токен получен через API")
                    return f"Bearer {token}"

            print(f"❌ API авторизация не удалась: {response.status_code}")
            return None

        except Exception as e:
            print(f"❌ Ошибка API авторизации: {e}")
            return None

    def get_valid_token(self, email=None, password=None):
        """🎯 ГЛАВНЫЙ МЕТОД: Получить валидный токен"""

        # 1. 🔍 Проверяем кэш
        token = self.get_cached_token()
        if token:
            return token

        print("🔄 Получение нового токена...")

        # 2. 🖥️ Пробуем получить через браузер
        token = self.get_token_from_browser_storage()
        if token:
            self.save_token_to_cache(token)
            return token

        # 3. 🔑 Пробуем получить через API (если есть креды)
        if email and password:
            token = self.get_token_via_api(email, password)
            if token:
                self.save_token_to_cache(token)
                return token

        # 4. ❌ Все методы не сработали
        print("❌ Не удалось получить токен автоматически")
        print("💡 Войди вручную на сайт и обнови токен в .env файле")
        return None

    def test_token(self, token):
        """🧪 Проверить валидность токена"""
        if not token:
            return False

        test_url = f"{self.api_url}/v1/cart/short"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "*/*",
            "Authorization": token
        }

        try:
            response = requests.get(test_url, headers=headers, timeout=10)
            return response.status_code == 200
        except:
            return False


# 📦 Создаем глобальный экземпляр менеджера токенов
token_manager = TokenManager()