from bs4 import BeautifulSoup
from melhores_destinos import static
import re
import json

class Parser():

    def _soup(self, raw_data):
        return BeautifulSoup(raw_data.text, 'html.parser')

    def get_urls_destinos(self, response):
        soup = self._soup(response)
        result_div = soup.find('div',{'class':'coluna-lista-promos'})
        result_lis = result_div.find_all('li')
        final_lis = []
        for i, li in enumerate(result_lis):
            result_span = li.find('span',{'class':'categoria-publicacao'})
            for country in static.COUTRYS:
                if result_span is not None and country in result_span.text.upper() and self._is_valor_valido(li):
                    final_lis.append(li)
        return self._get_urls_by_lis(final_lis)

    def _get_urls_by_lis(self, final_lis):
        result_a = []
        for li in final_lis:
            a = li.find('a')
            if a is None:
                continue
            result_a.append(a.get('href'))
        return result_a

    def _is_valor_valido(self, li):
        valor = re.search(r"R\$ \d{1}.\d{3}", li.find('p').text)
        if valor is None:
            return False
        return 2000 > self._str_to_int_valor_passagem(valor.group())

    def _str_to_int_valor_passagem(self, raw_data):
        return float(raw_data.replace('R$', '').replace('.', '').strip())


    def get_keys(self, response):
        raw_json = re.search(r"var promo = (\{.*\})", response.text)
        structured_data = json.loads(raw_json.group(1))
        if structured_data is None:
            return None
        return structured_data.get('key')


    def is_promocao_valida(self, responses):
        for result in responses.get('resumo_tarifas_ativas'):
            city = static.CITYS.get(result.get('from_city_code'))
            if city is not None and city > result.get('total_price'):
                return True

    
    def _is_valor(self, valor, city_valor):
        return valor < city_valor

        