"""
API клиент для Читай-город с адаптером ответов - КОНТРОЛИРУЕМЫЕ ЛОГИ
"""
import requests
import logging
from config import settings, tokens

# Создаем логгер только для важных событий API
api_logger = logging.getLogger('api')


class ApiResponseAdapter:
    """Преобразует JSON:API в чистый формат"""

    @staticmethod
    def adapt_search_response(api_response):
        """Адаптирует ответ поиска"""
        if "status" in api_response:
            return {"ok": False, "status": api_response["status"]}

        if "data" not in api_response:
            return {"ok": False, "error": "No data"}

        data = api_response["data"]
        included = api_response.get("included", [])

        # Собираем детали продуктов
        products_details = {item["id"]: item.get("attributes", {})
                          for item in included if item.get("type") == "product"}

        # Получаем продукты из relationships
        products_data = data.get("relationships", {}).get("products", {}).get("data", [])
        pagination = data.get("relationships", {}).get("products", {}).get("meta", {}).get("pagination", {})

        # Формируем книги
        books = []
        for product_ref in products_data:
            product_id = product_ref.get("id")
            if product_id in products_details:
                details = products_details[product_id]

                # Автор
                authors = details.get("authors", [])
                author = " ".join(filter(None, [
                    authors[0].get("lastName") if authors else "",
                    authors[0].get("firstName") if authors else "",
                    authors[0].get("middleName") if authors else ""
                ])) if authors else "Неизвестный автор"

                # Скидка
                discount = details.get("discount")
                discount_str = f"{discount}%" if discount else None

                books.append({
                    "id": product_id,
                    "title": details.get("title", "Без названия"),
                    "author": author,
                    "price": details.get("price", 0),
                    "old_price": details.get("oldPrice"),
                    "discount": discount_str,
                    "available": details.get("status") == "canBuy",
                    "category": details.get("category", {}).get("title", "Без категории"),
                    "publisher": details.get("publisher", {}).get("title", ""),
                    "rating": float(details.get("rating", {}).get("count", "0.0"))
                })

        return {
            "ok": True,
            "found": len(books),
            "total": pagination.get("total", len(books)),
            "books": books
        }

    @staticmethod
    def adapt_popular_searches_response(api_response):
        """Адаптирует популярные запросы"""
        if "status" in api_response:
            return {"ok": False, "status": api_response["status"]}

        if "data" not in api_response:
            return {"ok": False, "error": "No data"}

        # Собираем фразы
        phrases = [
            {"id": item.get("id"), "text": item.get("attributes", {}).get("phraseText", "")}
            for item in api_response.get("included", [])
            if item.get("type") == "popularSearchPhrase" and item.get("attributes", {}).get("phraseText")
        ]

        return {"ok": True, "count": len(phrases), "phrases": phrases}


class ChitaiGorodAPIClient:
    """API клиент с адаптером - КОНТРОЛИРУЕМЫЕ ЛОГИ"""

    def __init__(self, use_auth=True, base_url=settings.API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.adapter = ApiResponseAdapter()
        self.city_id = settings.DEFAULT_CITY_ID

        # Заголовки
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, */*",
            "Referer": f"{settings.BASE_URL}/",
        })

        if use_auth and tokens.AUTH_TOKEN:
            token = tokens.AUTH_TOKEN
            if "Bearer%20" in token:
                token = token.replace("Bearer%20", "Bearer ")
            elif not token.startswith("Bearer "):
                token = f"Bearer {token}"
            self.session.headers.update({"Authorization": token})

        # Логируем только факт создания клиента
        api_logger.info("🔧 API клиент инициализирован")

    def _request(self, method, endpoint, **kwargs):
        """Базовый запрос - ЛОГИРУЕМ ТОЛЬКО ВАЖНОЕ"""
        url = self.base_url + endpoint
        kwargs.setdefault("timeout", settings.TIMEOUT)

        # Логируем только метод и эндпоинт (без деталей)
        api_logger.debug(f"📤 {method} {endpoint}")

        response = self.session.request(method, url, **kwargs)

        # Логируем только статус код (не весь ответ)
        if response.status_code == 200:
            api_logger.debug(f"📥 Ответ: {response.status_code} OK")
        else:
            api_logger.warning(f"📥 Ответ: {response.status_code} ERROR")

        return response

    def search_products(self, phrase, page=1, per_page=20):
        """Поиск товаров - ЛОГИРУЕМ РЕЗУЛЬТАТ"""
        params = {
            "customerCityId": self.city_id,
            "products[page]": page,
            "products[per-page]": per_page,
            "phrase": phrase,
        }

        # Логируем факт поиска
        api_logger.info(f"🔍 Поиск: '{phrase[:20]}...'")

        response = self._request("GET", settings.PUBLIC_API_ENDPOINTS["SEARCH_PRODUCT"], params=params)

        if response.status_code == 200:
            result = self.adapter.adapt_search_response(response.json())

            # Логируем результат поиска
            if result.get("ok"):
                api_logger.info(f"✅ Найдено: {result.get('found')} товаров")
            else:
                api_logger.warning(f"❌ Поиск неудачен: {result.get('status')}")

            return result
        else:
            api_logger.error(f"❌ Ошибка API: {response.status_code}")
            return {"ok": False, "status": response.status_code}

    def get_popular_searches(self):
        """Популярные запросы - ЛОГИРУЕМ РЕЗУЛЬТАТ"""
        api_logger.info("🔥 Запрос популярных поисков")

        response = self._request("GET", settings.PUBLIC_API_ENDPOINTS["POPULAR_SEARCHES"])

        if response.status_code == 200:
            result = self.adapter.adapt_popular_searches_response(response.json())

            if result.get("ok"):
                api_logger.info(f"✅ Получено фраз: {result.get('count')}")
            else:
                api_logger.warning(f"❌ Не удалось получить популярные запросы")

            return result
        else:
            api_logger.error(f"❌ Ошибка API: {response.status_code}")
            return {"ok": False, "status": response.status_code}