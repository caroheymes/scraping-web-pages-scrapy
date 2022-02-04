# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Identity
from w3lib.html import remove_tags,strip_html5_whitespace, replace_escape_chars,strip_html5_whitespace,get_base_url
import re
from unidecode import unidecode



class GrabItem(scrapy.Item):
    def remove_script_code(data):
        clean = re.compile('<script>.*?</script>')
        return [re.sub(clean, '', data)]

    def remove_style_code(data):
        clean = re.compile('<style>.*?</style>')
        return [re.sub(clean, '', data)]
        
    def remove_style(data):
        # clean = re.compile('{.*?}')
        # return [re.sub(clean, '', data)]
        return "".join(re.split("\(|\)|\[|\]|\{|\}", data)[::2])

    def remove_media(data):
        clean = re.compile(' @media .*?) ')
        return [re.sub(clean, '', data)]

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
    def super_join(liste):
        return ' '.join(liste)

    # define the fields for your item here like:
    # name = scrapy.Field()
    index  = scrapy.Field()

    base_url  = scrapy.Field()

    origin_url = scrapy.Field()

    title = scrapy.Field(
        input_processor = MapCompose(stripn),
        output_processor = TakeFirst()
    )
    h1 = scrapy.Field(        
        input_processor = MapCompose( remove_tags, strip_html5_whitespace),
        output_processor = TakeFirst()
        )
    h2 = scrapy.Field(
        input_processor = MapCompose(remove_style_code, 
                                    remove_script_code, 
                                    remove_style,  
                                    strip_html5_whitespace,
                                    remove_tags, 
                                    remove_space ),
        output_processor = Join()
    )
                            
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