from passagens_imperdiveis import spider as spiderPassagem
from melhores_destinos import spider as spiderMelhores

if __name__ == "__main__":
    print('COMEÇOU')
    melhores = spiderMelhores.Spider()
    passagens = spiderPassagem.Spider()
    passagens.start_crawling()
    melhores.start_crawling()
    print('FINALIZADO')
