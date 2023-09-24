import requests
import json
from config import keys# импортируем keys в этот фаил
class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException('\nНевозможно перевести'
                                      f'\nодинаковые валюты: {base}.\n'
                                      '\nУвидеть доступные'
                                      '\nвалюты → /values\n'
                                      '\nФормула записи для'
                                      '\nперевода валюты → /help')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException('\nНе удалось обработать\n'
                                      f'валюту {quote}\n'
                                      '\nУвидеть доступные'
                                      '\nвалюты → /values\n'
                                      '\nФормула записи для'
                                      '\nперевода валюты → /help')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException('\nНе удалось обработать\n'
                                      f'валюту {base}\n'
                                      '\nУвидеть доступные'
                                      '\nвалюты → /values\n'
                                      '\nФормула записи для'
                                      '\nперевода валюты → /help')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException('\nНе удалось обработать\n'
                                      f'количество {amount}.\n'
                                      '\nУвидеть доступные'
                                      '\nвалюты → /values\n'
                                      '\nФормула записи для'
                                      '\nперевода валюты → /help')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = round((json.loads(r.content)[keys[base]])*float(amount),2)

        return total_base