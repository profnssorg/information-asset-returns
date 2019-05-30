"""

Nome: Spider G1
Objetivo: Coletar informações -título, texto e data - para cada uma
das notícias sonbre política presentes no site do G1
Autor: Bernardo Paulsen
Data: 31/03/2019
Versão: 1.0.0
Detalhes versão: Tudo certo 


O q vai fazer
    Entrada: "https://g1.globo.com/politica/"
    Saída: arquivo de texto com informações (titulo, data e link)
    sobre todas as notícias publicadas no site de entrada.
    Processamento: classe .Spyder vai buscar pelas informações
Planejamento de código:
    Procurar, no site, os links para ir para as paginas das noiticas
    publicadas, e também para ir até a próxima página de noticias.
    Nas páginas das noticias, coletar titulo, data e link. Na
    próxima página de noticias, repetir o processo. Parar quando
    houver mais uma próxima página.


"""

import scrapy

n = 1

class news3(scrapy.Spider):
    name = 'g1'
    start_urls = ['https://g1.globo.com/politica/']

    def parse(self, response):
        global n
        # follow links to news pages
        for page in response.xpath('//div/div[2]/div/div/a/@href').getall():
            yield response.follow(page, self.parse_noticia)

        # follow pagination links
        n += 1
        if n <= 2000:
            next_page = ("https://g1.globo.com/politica/index/feed/pagina-%d.ghtml" % (n))
            yield response.follow(next_page, self.parse)

    def parse_noticia(self, response):
        yield {
            'data': response.xpath('//time/text()')[0].get(),
            'titulo': response.xpath('//h1/text()')[2].get(),
            'link': response.url,
            }

