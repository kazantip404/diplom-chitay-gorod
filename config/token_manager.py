import requests
import json
import os
from datetime import datetime, timedelta


class TokenManager:
    def __init__(self):
        self.token_file = "config/token_cache.json"
        self.token = None
        self.expires_at = None

    def get_token(self):
        """🔑 ПОЛУЧЕНИЕ ТОКЕНА (из кэша или нового)"""
        # Пробуем загрузить из кэша
        if self._load_cached_token():
            return self.token

        # Получаем новый токен
        return self._get_new_token()

    def _load_cached_token(self):
        """📁 ЗАГРУЗКА ТОКЕНА ИЗ КЭША"""
        try:
            if os.path.exists(self.token_file):
                with open(self.token_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Проверяем срок действия (24 часа)
                expires_str = data.get('expires_at')
                if expires_str and datetime.fromisoformat(expires_str) > datetime.now():
                    self.token = data['token']
                    self.expires_at = datetime.fromisoformat(expires_str)
                    print("✅ Токен загружен из кэша")
                    return True
                else:
                    print("⚠️ Токен в кэше устарел")

        except Exception as e:
            print(f"❌ Ошибка загрузки токена из кэша: {e}")

        return False

    def _save_token_to_cache(self, token, expires_in=86400):  # 24 часа
        """💾 СОХРАНЕНИЕ ТОКЕНА В КЭШ"""
        try:
            expires_at = datetime.now() + timedelta(seconds=expires_in)

            data = {
                'token': token,
                'expires_at': expires_at.isoformat(),
                'updated_at': datetime.now().isoformat()
            }

            os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
            with open(self.token_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print("✅ Токен сохранен в кэш")

        except Exception as e:
            print(f"❌ Ошибка сохранения токена: {e}")

    def _get_new_token(self):
        """🆕 ПОЛУЧЕНИЕ НОВОГО ТОКЕНА"""
        try:
            # 🔐 Пробуем получить токен через API
            token = self._get_token_from_api()

            if token:
                self.token = token
                self._save_token_to_cache(token)
                return token

        except Exception as e:
            print(f"❌ Ошибка получения токена: {e}")

        # 🔐 Используем статический токен как запасной вариант
        return self._get_static_token()

    def _get_token_from_api(self):
        """🔐 ПОПЫТКА ПОЛУЧЕНИЯ ТОКЕНА ЧЕРЕЗ API"""
        # ⚠️ Для Читай-города API получения токена может быть закрытым
        # В реальном проекте здесь будет логика авторизации
        print("⚠️ API получения токена недоступно, используем статический")
        return None

    def _get_static_token(self):
        """🔄 СТАТИЧЕСКИЙ ТОКЕН"""
        # Токен из вашего сообщения
        static_token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3VzZXItcmlnaHQiLCJzdWIiOjIyOTc3ODE3LCJpYXQiOjE3NjQwODczMTAsImV4cCI6MTc2NDA5MDkxMCwidHlwZSI6MjAsImp0aSI6IjAxOWFiYmNjLTI4N2UtNzM3ZC1hOThhLWM4YzNhYjdkZGEzZCIsInJvbGVzIjoxMH0.x4yDWLIuhZqUbfhGcSZY4p1_ajjX34c0tZr231beeB8"

        # Сохраняем статический токен в кэш
        self._save_token_to_cache(static_token)
        return static_token


# ✅ ГЛОБАЛЬНЫЙ ЭКЗЕМПЛЯР
token_manager = TokenManager()