# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # Here we define the fields for our item 
    title = scrapy.Field()
    contents = scrapy.Field()
    url = scrapy.Field()
