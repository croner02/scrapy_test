# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZiroomItem(scrapy.Item):
    title = scrapy.Field()
    href = scrapy.Field()
    desc = scrapy.Field()
    location = scrapy.Field()
    price = scrapy.Field()
