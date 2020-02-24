import requests
from melhores_destinos import static, parser
from emailPromo import Email
import json


class Spider():
    _BASE_URL = [
        'https://passagensaereas.melhoresdestinos.com.br/promocoes?page=1',
        'https://passagensaereas.melhoresdestinos.com.br/promocoes?page=2',
        'https://passagensaereas.melhoresdestinos.com.br/promocoes?page=3',
    ]

    def __init__(self):
        self.parser = parser.Parser()
        self.email_send = Email()

    def start_crawling(self):
        response = []
        for url_crawling in self._BASE_URL:
            response = requests.get(
                url=url_crawling,
                headers=static.HEADERS
            )
            self._requests_for_urls(self.parser.get_urls_destinos(response))


    def _requests_for_urls(self, urls):
        send = []
        for url in urls:
            response = (requests.get(
                url=url,
                headers=static.HEADERS
            ))

            key = self.parser.get_keys(response)
            if key is None:
                continue
            data_json = self._requests_for_keys(key)
            if self.parser.is_promocao_valida(data_json):
                send.append(response.url)

        if len(send) != 0:
            self.email_send.send_email(send)
            

    def _requests_for_keys(self, key):
        response = (requests.get(
            url=f'https://passagensaereas.melhoresdestinos.com.br/cheapest_prices_json?key={key}',
            headers=static.HEADERS
        ))
        if response is None or response.status_code == 404:
            return None
        return json.loads(response.text)
