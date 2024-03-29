import requests
import json
from config import keys

class ConvertionException(Exception):
    pass
class APIException:
    @staticmethod
    def convert(quote:str, base:str, amount:str):
        if quote == base:
            raise ConvertionException('Указана одинаковая валюта')

        if float(amount) <0:
            raise ConvertionException('Неверно указано кол-во валюты')

        try:
            amount = float(amount)
        except:
            raise ConvertionException('Неверно указано кол-во валюты')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось найти валюту: {quote}. Список достпных валют: /values')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось найти валюту: {base}. Cписок достпных валют: /values')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/887567339b823d15b5f7b282/pair/{quote_ticker}/{base_ticker}/{amount}')
        result = json.loads(r.content)

        return result