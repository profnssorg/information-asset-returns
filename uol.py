import scrapy
from scrapy_splash import SplashRequest
from scrapy.selector import Selector


class ExampleSpider(scrapy.Spider):
    name = 'uol'
    script='''
function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  for i=1,50,1
  do
    assert(splash:runjs('document.querySelector("body > section > div > div > div.col-sm-24.col-md-16.col-lg-17 > section > div > div.element-divisor > div > button").click()'))
    assert(splash:wait(0.5))
  end
  splash:set_viewport_full()
  return splash:html()
end
    '''

    def start_requests(self):
        url = 'https://noticias.uol.com.br/politica/'
        yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={'wait':0.5, 'lua_source': self.script})

    def parse(self, response):
        page = response.body
        sel = Selector(text=page)
        for noticia in sel.xpath('//section/div/div/div[1]/section/div/div[1]/div/div/a'):
            yield{
            'data': noticia.xpath('.//time/text()').get(),
            'titulo': noticia.xpath('.//h3/text()').get(),
            'link': noticia.xpath('.//@href').get()
            }