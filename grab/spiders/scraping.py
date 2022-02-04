import scrapy
import pandas as pd
from ..items import GrabItem
import json
from scrapy.loader import ItemLoader



class ScrapingSpider(scrapy.Spider):
    
    name = 'grab'
    # allowed_domains = ['example.com']

    

    def start_requests(self):
        my_file = "C:/Users/carol/Desktop/grab/grab/websites.csv"
        df = pd.read_csv(my_file)
        start_urls = [x for x in df.website]
        for index, url in enumerate( start_urls):
            yield scrapy.Request(url, callback=self.parse, cb_kwargs={'index':index,'base_url' : url})


    def parse(self, response, index, base_url):   
        

        l= ItemLoader(item= GrabItem(), response = response)
        l.add_value('index', index)
        l.add_value('base_url', base_url)
        # l.add_value('final_url', response.url)
        l.add_xpath('title', '//title/text()')
        l.add_xpath('h1', '//h1/text()')
        l.add_xpath('h2', '//h2/text()')
        l.add_xpath('header_links_text',  '//header//a/text()')
        l.add_xpath('body_text', '//body//div//text() |//body//span//text() | //body//p//text() | //body//li//text() | //body/..//section/text()')
        # items ={
        #     'index' : index,
        #     'base_url' : base_url,
        #     'final_url' : final_url,
        # }
        # yield items
        yield l.load_item()


