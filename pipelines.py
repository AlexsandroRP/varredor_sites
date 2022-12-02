
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

# class VarredorSitesPipeline:
#     def process_item(self, item, spider):
#         return item

class SQLitePipeline(object):
    def open_spider(self, spider):
        self.connection = sqlite3.connect('proxies.db') #define conexão com o DB, proxies nome que vc da ao banco
        self.cursor = self.connection.cursor() # permite fazer pesquisas e alterações gerais no DB
        # Criar a tabela
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS proxies(
                ip_adress TEXT NOT NULL PRIMARY KEY,
                port NUMBER,
                code TEXT,
                country TEXT,
                anonimity TEXT,
                google TEXT,
                https TEXT,
                last_checked TEXT
            )
        ''')
        self.connection.commit() # Envia as infos para o DB

    def close_spider(self, spider):
        self.connection.close() # fechar a conexão
    
    # colunas que estarão recebendo dados
    def process_item(self, item, spider):
        self.cursor.execute('''
            INSERT OR IGNORE INTO proxies(ip_adress,port,code,country,anonimity,google,https,last_checked) VALUES(?,?,?,?,?,?,?,?)
        ''', (
            item.get('ip_adress'),
            item.get('port'),
            item.get('code'),
            item.get('country'),
            item.get('anonimity'),
            item.get('google'),
            item.get('https'),
            item.get('last_checked'),
        ))
        # 8 ? de acordo com a qtde de colunas passadas

        # Salvar no DB
        self.connection.commit()
        return item