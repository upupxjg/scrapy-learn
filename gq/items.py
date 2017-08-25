# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GqItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()
    period = scrapy.Field()
    lang = scrapy.Field()
    uptime = scrapy.Field()
    region = scrapy.Field()
    mv_class = scrapy.Field()
    imdb_s = scrapy.Field()
    imdb_url = scrapy.Field()
    douban_s = scrapy.Field()
    douban_url = scrapy.Field()
    mv_length = scrapy.Field()
    mv_poster = scrapy.Field()
    director = scrapy.Field()
    actor = scrapy.Field()
    desc = scrapy.Field()
    magnet = scrapy.Field()