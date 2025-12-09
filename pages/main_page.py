from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure


class MainPage(BasePage):
    """🏠 ГЛАВНАЯ СТРАНИЦА сайта Читай-город"""

    # 🎯 ЛОКАТОРЫ ЭЛЕМЕНТОВ - ЗАМЕНИ НА РЕАЛЬНЫЕ С ТВОЕГО САЙТА!
    # Используй браузер -> Inspect -> Copy -> Copy selector

    # 🔍 ПОИСКОВАЯ СТРОКА - найди на сайте и подставь правильные селекторы
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='искать'], input[type='search'], .search-input")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], .search-btn, .search-button")

    # 🛒 КОРЗИНА - найди иконку корзины на сайте
    CART_ICON = (By.CSS_SELECTOR, ".cart-icon, [href*='cart'], .basket-icon")

    # 👤 КНОПКА ВХОДА - найди кнопку "Войти" или "Личный кабинет"
    LOGIN_BUTTON = (By.CSS_SELECTOR, ".login-btn, [href*='login'], .auth-btn, .user-profile")

    @allure.step("Открыть главную страницу")
    def open(self):
        """🚀 Открыть главную страницу сайта"""
        self.driver.get(self.config.BASE_URL)
        return self

    @allure.step("Выполнить поиск по запросу: {search_term}")
    def search_for(self, search_term):
        """🔍 Выполнить поиск и перейти на страницу результатов"""
        self.type_text(self.SEARCH_INPUT, search_term)
        self.click(self.SEARCH_BUTTON)

        # 🔄 Возвращаем страницу поиска для дальнейших действий
        from pages.search_page import SearchPage
        return SearchPage(self.driver)

    @allure.step("Перейти в корзину")
    def go_to_cart(self):
        """🛒 Перейти в корзину"""
        self.click(self.CART_ICON)
        from pages.cart_page import CartPage
        return CartPage(self.driver)

    @allure.step("Открыть форму авторизации")
    def open_login_form(self):
        """👤 Открыть форму входа/регистрации"""
        self.click(self.LOGIN_BUTTON)
        from pages.auth_page import AuthPage
        return AuthPage(self.driver)