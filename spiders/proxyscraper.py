import scrapy

class ProxyScraperSpider(scrapy.Spider):
    # identidade
    name = 'proxyscraper'
    # request
    def start_requests(self):
        urls = ['https://www.us-proxy.org/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,meta={'next_url':urls[0]})
    
    # response
    def parse(self, response):    
        # Montar um xpath que retorna a linha
        for linha in response.xpath("//table[@class='table table-striped table-bordered']//tr"): # itera em todos os tr
            yield{
                # Montar individualmente um xpath que retorna cada item daquela linha
                'ip_Address': linha.xpath("./td[1]/text()").get(), # itera sobre cada uma das colunas
                'port': linha.xpath("./td[2]/text()").get(), # itera sobre cada uma das colunas
                'code': linha.xpath("./td[3]/text()").get(), # itera sobre cada uma das colunas
                'country': linha.xpath("./td[4]/text()").get(), # itera sobre cada uma das colunas
                'anonymity': linha.xpath("./td[5]/text()").get(), # itera sobre cada uma das colunas
                'google': linha.xpath("./td[6]/text()").get(), # itera sobre cada uma das colunas
                'https': linha.xpath("./td[7]/text()").get(), # itera sobre cada uma das colunas
                'last_checked': linha.xpath("./td[8]/text()").get(), # itera sobre cada uma das colunas
            }
            