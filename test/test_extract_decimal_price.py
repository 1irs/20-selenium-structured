import unittest
from decimal import Decimal

from page_object.search_page import extract_decimal_price


class ExtractDecimalPriceTest(unittest.TestCase):

    def test(self):
        examples = [
            # 0                                 1
            ["$110.00 $122.00\nEx Tax: $90.00", Decimal(110.0)],
            ["$98.00 $122.00\nEx Tax: $80.00",  Decimal(98.0)],
            ["$122.00\nEx Tax: $100.00",        Decimal(122.0)],
            ["$1,202.00\nEx Tax: $1,000.00",    Decimal(1202.0)],
        ]

        for example in examples:
            self.assertEqual(example[1], extract_decimal_price(example[0]))
