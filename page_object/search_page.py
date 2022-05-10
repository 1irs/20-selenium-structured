from dataclasses import dataclass
from decimal import Decimal
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select


def extract_decimal_price(text: str) -> Decimal:
    """Функция, которая извлекает из строки цену"""
    """Примеры:
    $110.00 $122.00
    Ex Tax: $90.00
    $98.00 $122.00
    Ex Tax: $80.00
    $122.00
    Ex Tax: $100.00"""

    # text == "$110.00 $122.00\nEx Tax: $90.00"
    split_by_lines: List[str] = text.split("\n")
    # split_by_lines == ["$110.00 $122.00", "Ex Tax: $90.00"]

    first_price_lines = split_by_lines[0].split(' ')
    # first_price == ["$110.00", "$122.00"]

    # Удаляем первый символ (доллар)
    first_price = first_price_lines[0][1:]
    # В случае 1,202.00 нужно убрать запятую.
    first_price_without_punctuation = first_price.replace(",", "")

    return Decimal(first_price_without_punctuation)


@dataclass
class ProductInfo:
    name: str
    price: Decimal


class SearchPage:

    url = 'http://tutorialsninja.com/demo/index.php?route=product/category&path=20'

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_sort_input(self) -> WebElement:
        return self.driver.find_element(By.ID, 'input-sort')

    def sort_price_low_high(self):
        select = Select(self.get_sort_input())
        select.select_by_visible_text('Price (Low > High)')

    def sort_price_high_low(self):
        select = Select(self.get_sort_input())
        select.select_by_visible_text('Price (High > Low)')

    def sort_name_az(self):
        select = Select(self.get_sort_input())
        select.select_by_visible_text('Name (A - Z)')

    def sort_name_za(self):
        select = Select(self.get_sort_input())
        select.select_by_visible_text('Name (Z - A)')

    def open(self):
        self.driver.get(self.url)

    def get_search_results(self) -> List[ProductInfo]:
        """Метод, который возвращает список моделей ProductInfo,
        в том порядке, в како они встречаются на странице."""

        # Получаем все теги <div class="product-layout ...">...</div>
        # со всем содержимым.
        products_tags = self.driver.find_elements(By.CLASS_NAME, 'product-layout')

        # Заводим пустой массив, куда будем накапливать информацию о продуктах.
        products: List[ProductInfo] = []

        # Перебираем все найденные теги с классом product-layout
        for product_div_tag in products_tags:

            # Внутри тега ищем тег <H4> — внутри него будет название продукта.
            name: str = product_div_tag.find_element(By.TAG_NAME, 'h4').text

            # Внутри тега ищем тег с классом price, внутри него будет информация о ценах.
            price_text: str = product_div_tag.find_element(By.CLASS_NAME, 'price').text

            # Создаем объект по модели продукта.
            product = ProductInfo(
                name=name,

                # Корректно выбираем первую цену из строки.
                price=Decimal(extract_decimal_price(price_text))
            )

            # Добавляем объект продукта в общий массив с продуктами.
            products.append(product)

        return products
