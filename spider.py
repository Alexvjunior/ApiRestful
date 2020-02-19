import requests
from parser import Parser
from emailPromo import Email


class Spider():
    _URL_MASTER = 'https://www.passagensimperdiveis.com.br/categoria/estados-unidos'

    def __init__(self):
        self.parser = Parser()
        self.email_send = Email()

    def start_crawling(self):
        print('COMEÇOU')
        response = requests.get(
            url=self._URL_MASTER
        )

        urls = self.parser.find_urls(response)
        self._request_promocao_passagem(urls)

    def _request_promocao_passagem(self, urls):
        responses = []
        for url in urls:
            responses.append(requests.get(
                url=url
            ))
        send = self.parser.verificar_promocao(responses)
        if send != None:
            self.email_send.send_email(send)


if __name__ == '__main__':
    spider = Spider()
    spider.start_crawling()
