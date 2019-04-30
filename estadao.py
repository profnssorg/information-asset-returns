import scrapy
from scrapy_splash import SplashRequest
from scrapy.selector import Selector

class ExampleSpider(scrapy.Spider):
    name = 'estadao'
    script='''
function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  for i=1,5000,1
  do
    assert(splash:runjs('document.querySelector("#ultimas > div > div > div > section > div > a").click()'))
    assert(splash:wait(0.01))
  end
  splash:set_viewport_full()
  return splash:html()
end
    '''

    def start_requests(self):
        url = 'https://politica.estadao.com.br/'
        yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={'wait':0.5, 'lua_source': self.script, 'timeout': 6000})

    def parse(self, response):
        page = response.body
        sel = Selector(text=page)
        for noticia in sel.xpath('//div/div/div/div[2]/section/div/div[2]/section[1]'):
            yield{
            'data': noticia.xpath('.//span[2]/text()').get(),
            'titulo': noticia.xpath('.//a/h3/text()').get(),
            'link': noticia.xpath('.//a/@href').get()
            }