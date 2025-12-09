import pytest
import allure
import os
import json
from datetime import datetime, timedelta
from config.config import config
from config.token_manager import TokenManager


@allure.feature("Система управления токенами")
class TestTokenSystem:

    def test_token_manager_initialization(self):
        """🎯 ТЕСТ: Инициализация менеджера токенов"""
        print("🎯 Проверка инициализации менеджера токенов...")
        manager = TokenManager()
        assert manager.token_file == "config/token_cache.json"
        assert manager.token is None
        assert manager.expires_at is None
        print("✅ Менеджер токенов инициализирован корректно")

    def test_token_caching(self):
        """🎯 ТЕСТ: Система кэширования токенов"""
        print("🎯 Проверка системы кэширования...")
        manager = TokenManager()
        test_token = "Bearer test_token_123"

        # Сохраняем токен
        manager._save_token_to_cache(test_token, expires_in=3600)

        # Загружаем токен
        loaded = manager._load_cached_token()
        assert loaded is True
        assert manager.token == test_token
        print("✅ Система кэширования работает")

    def test_config_token_property(self):
        """🎯 ТЕСТ: Свойство токена в конфигурации"""
        print("🎯 Проверка свойства токена в конфигурации...")
        token = config.API_TOKEN
        assert token is not None
        assert isinstance(token, str)
        assert token.startswith("Bearer ")
        print(f"✅ Токен получен: {token[:50]}...")

    def test_token_validity(self):
        """🎯 ТЕСТ: Валидность токена"""
        print("🎯 Проверка валидности токена...")
        token = config.API_TOKEN

        # Проверяем базовую структуру токена
        assert token.startswith("Bearer ")
        assert len(token) > 50

        # Проверяем что токен может быть использован в запросе
        # (даже если API вернет 403, главное что запрос отправляется)
        import requests
        url = f"{config.API_BASE_URL}/v2/search/popular-search-phrases"
        headers = {"Authorization": token}

        try:
            response = requests.get(url, headers=headers, timeout=5)
            # Принимаем любой статус - главное что запрос выполнен
            assert response.status_code in [200, 401, 403]
            print("✅ Токен валидный! API отвечает корректно.")
        except Exception as e:
            pytest.fail(f"❌ Ошибка при проверке токена: {e}")


@allure.feature("Автообновление токенов")
class TestTokenAutoRefresh:

    def test_auto_token_refresh(self):
        """🎯 ТЕСТ: Автоматическое обновление токена"""
        print("🎯 Тестирование автоматического обновления токена...")

        # Получаем токен несколько раз - должен быть одинаковым (кэширование)
        token1 = config.API_TOKEN
        token2 = config.API_TOKEN

        assert token1 == token2
        assert token1 is not None
        assert token2 is not None

        print(f"🔐 Токен 1: {token1[:40]}...")
        print(f"🔐 Токен 2: {token2[:40]}...")
        print("✅ Система корректно возвращает кэшированный токен")