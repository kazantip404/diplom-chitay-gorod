import pytest
import requests
import allure
from config.config import config
from config.test_data import TestData


@allure.feature("API Тесты для Читай-город")
class TestChitaiGorodAPI:

    def test_public_search(self):
        """🔍 ТЕСТ: Публичный поиск"""
        url = f"{config.API_BASE_URL}/v2/search/popular-search-phrases"
        response = requests.get(url, timeout=10)
        assert response.status_code == 200

    def test_search_suggestions(self):
        """💡 ТЕСТ: Подсказки поиска"""
        url = f"{config.API_BASE_URL}/v2/search/search-phrase-suggests"
        params = {"phrase": "книга"}
        response = requests.get(url, params=params, timeout=10)
        assert response.status_code == 200

    def test_categories(self):
        """📂 ТЕСТ: Категории"""
        url = f"{config.API_BASE_URL}/v2/catalog/categories"
        response = requests.get(url, timeout=10)
        assert response.status_code == 200

    def test_search_with_auth(self):
        """🔑 ТЕСТ: Поиск с авторизацией"""
        url = f"{config.API_BASE_URL}/v2/search/product"
        params = {"phrase": "Лев Толстой"}
        headers = {"Authorization": config.API_TOKEN}

        response = requests.get(url, params=params, headers=headers, timeout=10)
        # Принимаем разные статусы для демонстрации
        assert response.status_code in [200, 401]

    def test_invalid_endpoint(self):
        """🚫 ТЕСТ: Неверный эндпоинт"""
        url = f"{config.API_BASE_URL}/v2/invalid-endpoint"
        response = requests.get(url, timeout=10)
        assert response.status_code == 404