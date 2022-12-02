# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join

def tirar_espaco_branco(valor):
    return valor.strip() # retira os valores em branco do string

def processar_caracteres_especiais(valor):
    return valor.replace(u"\u2019",'').replace(u"\u201d",'').replace(u"\u2014",'-') # Afunção irá remover os caracteres especiais varridos no site pelos valores ''

def colocar_nome_maisculo(valor):
    return valor.upper()    

class CitacaoItem(scrapy.Item):
    # formatar o resultado da varredura das citações, colocar somente os campos que deseja processar/formatar
    frase = scrapy.Field(
        input_processor=MapCompose(tirar_espaco_branco, processar_caracteres_especiais), # Quando o dado entra. passa as funções para processamento dos textos varridos
        
        # Quando o dado sai...
        output_processor=TakeFirst() # Retorna o resultado após formatações
    )
    autor = scrapy.Field(
        input_processor=MapCompose(colocar_nome_maisculo, tirar_espaco_branco),
        
        output_processor=TakeFirst() # nesse caso sem necessidade de formatações
    )
    tags = scrapy.Field(
        output_processor=Join(';') # une as tags somente em ';', não mais em lista
    )
    
