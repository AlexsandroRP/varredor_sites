import scrapy
from scrapy.loader import ItemLoader # essencial para importar as funcionalidades de formatação criada em items.py
from varredor_sites.items import CitacaoItem # classe criada em items.py


# forma 1

# # CamelCase
# class QuotestoScrapeSpider(scrapy.Spider):
#     # Identidade
#     name = 'frasebot'  

#     # Request
#     def start_requests(self):
#         urls = ['https://www.goodreads.com/quotes'] # urls que serão varridos
#         # varrer todos os sites em urls
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse) # retorna os resultados na medida que vai encontrando

#     # Response
#     def parse(self, response):
#         # aqui é onde deve processar o que é retornado da response
#         for elemento in response.xpath("//div[@class='quote']"):
#             yield{
#                 'citacoes': elemento.xpath(".//div[@class='quoteText']/text()").get(), # get pega somente o primeiro resultado do elemento
#                 'autor': elemento.xpath(".//span[@class='authorOrTitle']/text()").get(), # IMPORTANTE: . para obter somente o elemento relacionado ao que foi iterado no for.
#                 'tag': elemento.xpath(".//div[@class='greyText smallText left']/a/text()").getall() # getall retorna todas as tags do site
#             }

#         # Varrendo varias páginas
#         # Tentar encontrar o botção next, se encontrar = varrer
#         try: # para quando chegar na última pagina e não gerar erro
#             link_nextpage = response.xpath("//div/a[@class='next_page']/@href").get()
#             if link_nextpage is not None:
#                 link_nextpage_completo = response.urljoin(link_nextpage) # pega url definida em urls e junta com link da proxima page
#                 yield scrapy.Request(url=link_nextpage_completo, callback=self.parse) # faz quantas vezes for necessário para as próximas paginas
#         except:
#             # senão, parar a automação
#             print("Chegamos na última página")        
        

# Forma 2


class GoodReadsSpider(scrapy.Spider):
    # Identidade
    name = 'frasebot'
    # Request

    def start_requests(self):
        # Definir url(s) a varrer
        urls = ['https://www.goodreads.com/quotes?page=1']
        # 'https://www.goodreads.com/quotes?page=1
        # 'https://www.goodreads.com/quotes?page=2
        

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    # Response

    def parse(self, response):
        # aqui é onde você deve processar o que é retornado da response
        for elemento in response.xpath("//div[@class='quote']"):
            loader = ItemLoader(item=CitacaoItem(), selector=elemento, response=response)
            loader.add_xpath('frase',".//div[@class='quoteText']/text()")
            loader.add_xpath('autor',".//span[@class='authorOrTitle']/text()")
            loader.add_xpath('tags',".//div[@class='greyText smallText left']/a/text()")
            yield loader.load_item()
            # Caso esteja formatando o campo acima, não precisa mais as informações abaixo
            '''yield {
                'frase': elemento.xpath(".//div[@class='quoteText']/text()").get(),
                'autor': elemento.xpath(".//span[@class='authorOrTitle']/text()").get(),
                'tags': elemento.xpath(".//div[@class='greyText smallText left']/a/text()").getall(),
            }'''
        # Encontrar o link para a próxima página e extrair o número da próxima página
        numero_proxima_pagina = response.xpath("//a[@class='next_page']/@href").get().split('=')[1]
        print('#'*20)
        print(numero_proxima_pagina)
        print('#'*20)
        if numero_proxima_pagina is not None:
            link_proxima_pagina = f'https://www.goodreads.com/quotes?page={numero_proxima_pagina}'
            print('#'*20)
            print(link_proxima_pagina)
            print('#'*20)
            yield scrapy.Request(url=link_proxima_pagina,callback=self.parse)

        # Ver se ainda existe um próxima página
        # Navegar até aquela próxima página ou parar caso não haja mais páginas        