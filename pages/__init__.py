"""Пакет Page Object Model."""
from .base_page import BasePage
from .home_page import HomePage
from .search_page import SearchPage
from .product_page import ProductPage
from .cart_page import CartPage

__all__ = [
    'BasePage',
    'HomePage',
    'SearchPage',
    'ProductPage',
    'CartPage'
]