from bs4 import BeautifulSoup
import re
from lxml import etree
import json
from passagens_imperdiveis.citys import CITYS

class Parser():

    def find_urls(self, raw_data):
        soup = self._soup(raw_data)
        results = soup.select('.PI-infor-promo')
        urls = []
        for r in results:
            a = r.find('a')
            if a == None:
                continue   
            result = re.search(r"R\$ \d{1}.\d{3}", a.text)
            if result is None:
                continue

            valor_passagem = self._str_to_int_valor_passagem(result.group())

            if not self._verificar_valor_passagem(valor_passagem, 2000):
                continue

            urls.append(a.get('href'))
        return urls
            


    def _soup(self, raw_data):
        return BeautifulSoup(raw_data.text, 'html.parser')

    def _verificar_valor_passagem(self, valor_passagem, valor):
        return valor_passagem < valor

    def _str_to_int_valor_passagem(self, raw_data):
        return float(raw_data.replace('R$', '').replace('.', '').strip())


    
    def verificar_promocao(self, responses):
        urls = []
        for response in responses:
            raw_json = re.search(r"const pi_json = (\{.*\})", response.text)
            structured_data = json.loads(raw_json.group(1))
            result = structured_data.get('r')
            for i,r in enumerate(result.get('i')):
                for key, value in CITYS.items():
                    if r.get('os') == key and r.get('p') != None and r.get('p').get('t') <= value:
                        urls.append(response.url)

        if len(urls) == 0:
            return None

        with open('result.txt', 'a+') as file_url:
            file_url.write(str(urls))
            file_url.write('\n')
            file_url.close()
        return str(urls)