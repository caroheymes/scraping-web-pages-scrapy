# Scrapy code for scraping web pages
## Python code for scraping web pages tracking index and and original url

## Main improvements in scraping.py : 
```
import pandas as pd
from ..items import GrabItem
from scrapy.loader import ItemLoader

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
        l.add_xpath('title', '//title/text()')
        l.add_xpath('h1', '//h1/text()')
        l.add_xpath('h2', '//h2/text()')
        l.add_xpath('header_links_text',  '//header//a/text()')
        l.add_xpath('body_text', '//body//div//text() |//body//span//text() | //body//p//text() | //body//li//text() | //body/..//section/text()')
        yield l.load_item()
        

```
        
## Rotation of user agents in settings
        
```
data = requests.get('https://raw.githubusercontent.com/tamimibrahim17/List-of-user-agents/master/Chrome.txt').content
data = str(data).split('\\n')
user_agents = data[3:len(data)-1]
USER_AGENTS = user_agents

DOWNLOADER_MIDDLEWARES = {
'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
                          }
```
 
 ## Main improvement in Items processing :         

```
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Identity
from w3lib.html import remove_tags,strip_html5_whitespace, replace_escape_chars,strip_html5_whitespace,get_base_url
import re
from unidecode import unidecode

def remove_script_code(data):
        clean = re.compile('<script>.*?</script>')
        return [re.sub(clean, '', data)]

def remove_style_code(data):
        clean = re.compile('<style>.*?</style>')
        return [re.sub(clean, '', data)]

def remove_style(data):
ret     urn "".join(re.split("\(|\)|\[|\]|\{|\}", data)[::2])

        def stripn(x):
        x = unidecode(x)
        x = re.sub('\s{2,10000}',  ' ', x)
        x = remove_tags(x)
        x = strip_html5_whitespace(x)
        x = replace_escape_chars(x)
        trans_table = {ord(c): None for c in u'\r\n\t'}
        x =  ''.join(x.strip().translate(trans_table))
        x = re.sub('\s{2,10000}',  ' ', x)
        x = re.sub('@{3,2000}',  '', x)
        x = x.replace('@@@', '@@')
        return x

def remove_space(x):
        if x != '':
            return x

def remove_empty(liste):
        return [elem for elem in liste if elem != '' ]

body_text = scrapy.Field(
        input_processor = MapCompose(remove_style_code, 
                                    remove_script_code, 
                                    remove_style,  
                                    strip_html5_whitespace,
                                    remove_tags, 
                                    remove_space ),
        output_processor = Join())

header_links_text = scrapy.Field(
        input_processor = MapCompose(remove_style_code, 
                                    remove_script_code, 
                                    remove_style,  
                                    strip_html5_whitespace,
                                    remove_tags, 
                                    remove_space ),
        output_processor = Join()
                             )
```          
