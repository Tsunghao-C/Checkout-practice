from enum import Enum


class CurrencyCode(Enum):
    """
    maintain allowed currency code
    """
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"

Currency_decimal_places = {
    CurrencyCode.USD: 2,
    CurrencyCode.EUR: 2,
    CurrencyCode.GBP: 2,
    CurrencyCode.JPY: 0,
}