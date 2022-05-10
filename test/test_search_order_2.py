import unittest
from decimal import Decimal
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from page_object.search_page import SearchPage, ProductInfo


class SearchOrder2Test(unittest.TestCase):

    driver = None
    search_page = None

    @classmethod
    def setUpClass(cls) -> None:
        """Предустановка. Выполняется один раз перед всеми тестами."""
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # Предусловие: открыта страница поиска.
        cls.search_page = SearchPage(cls.driver)
        cls.search_page.open()

    def setUp(self) -> None:
        self.driver = SearchOrder2Test.search_page

    @classmethod
    def tearDownClass(cls) -> None:
        """Выполняется один раз после всех тестов"""
        cls.driver.quit()

    def test_price_low_high(self):
        """От дешевых к дорогим"""

        # Сортируем:
        self.search_page.sort_price_low_high()

        # Получаем список моделей
        products: List[ProductInfo] = self.search_page.get_search_results()

        # Самописный алгоритмический способ.
        # is_sorted = True
        # for i in range(0, len(products)-1):
        #    if products[i].price > products[i+1].price:
        #        is_sorted = False
        #        break

        prices: List[Decimal] = [product.price for product in products]

        self.assertNotEqual(sorted(prices), sorted(prices, reverse=True))
        self.assertEqual(prices, sorted(prices))

    def test_price_high_low(self):
        """От дорогих к дешевым"""

        # Сортируем от дорогих к дешевым.
        self.search_page.sort_price_high_low()

        # Получаем список моделей со страницы.
        products: List[ProductInfo] = self.search_page.get_search_results()

        # Проверяем, что отсортированы корректно.
        prices: List[Decimal] = [product.price for product in products]
        self.assertNotEqual(sorted(prices), sorted(prices, reverse=True))
        self.assertEqual(prices, sorted(prices, reverse=True))

    def test_name_az(self):
        """От а к я"""

        # Сортируем:
        self.search_page.sort_name_az()

        # Получаем список моделей
        products: List[ProductInfo] = self.search_page.get_search_results()

        names: List[str] = [product.name for product in products]

        self.assertNotEqual(sorted(names), sorted(names, reverse=True))
        self.assertEqual(names, sorted(names, key=str.lower))

    def test_name_za(self):
        """От я к а"""

        # Сортируем:
        self.search_page.sort_name_za()

        # Получаем список моделей
        products: List[ProductInfo] = self.search_page.get_search_results()

        names: List[str] = [product.name for product in products]

        self.assertNotEqual(sorted(names), sorted(names, reverse=True))
        self.assertEqual(names, sorted(names, reverse=True, key=str.lower))
