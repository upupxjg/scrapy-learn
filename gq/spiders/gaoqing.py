# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from gq.items import GqItem


class GaoqingSpider(CrawlSpider):
    name = 'gaoqing'
    allowed_domains = ['gaoqing.la']
    start_urls = ['http://gaoqing.la/']

    rules = (
        Rule(LinkExtractor(allow=r'.*\.html'),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        magnets = response.xpath('//a[contains(@href,"magnet")]')
        if len(magnets) > 0:
            content = response.xpath('//*[@id="post_content"]')
            item = GqItem()
            item['magnet'] = magnets.extract()
            item['mv_poster'] = content.xpath('./p[1]//@src').extract()
            actor_context = False
            desc_context = False
            actor = u''
            desc = u''
            for txt in content.xpath('./p/span//text()').extract():
                txt = txt.encode('utf-8')
                if '译　　名'.encode('utf-8') in txt:
                    item['name_en'] = txt[18:].decode('utf-8')
                elif '片　　名'.encode('utf-8') in txt:
                    item['name_zh'] = txt[18:].decode('utf-8')
                elif '年　　代'.encode('utf-8') in txt:
                    item['period'] = txt[18:].decode('utf-8')
                elif '产　　地'.encode('utf-8') in txt:
                    item['region'] = txt[18:].decode('utf-8')
                elif '类　　别'.encode('utf-8') in txt:
                    item['mv_class'] = txt[18:].decode('utf-8')
                elif '语　　言'.encode('utf-8') in txt:
                    item['lang'] = txt[18:].decode('utf-8')
                elif '上映日期'.encode('utf-8') in txt:
                    item['uptime'] = txt[18:].decode('utf-8')
                elif 'IMDb评分'.encode('utf-8') in txt:
                    item['imdb_s'] = txt[18:].decode('utf-8')
                elif 'IMDb链接'.encode('utf-8') in txt:
                    item['imdb_url'] = txt[18:].decode('utf-8')
                elif '豆瓣评分'.encode('utf-8') in txt:
                    item['douban_s'] = txt[18:].decode('utf-8')
                elif '豆瓣链接'.encode('utf-8') in txt:
                    item['douban_url'] = txt[18:].decode('utf-8')
                elif '片　　长'.encode('utf-8') in txt:
                    item['mv_length'] = txt[18:].decode('utf-8')
                elif '导　　演'.encode('utf-8') in txt:
                    item['director'] = txt[18:].decode('utf-8')
                elif '主　　演'.encode('utf-8') in txt:
                    actor_context = True
                    actor = actor + txt[18:].decode('utf-8') + '\n'
                elif '简　　介'.encode('utf-8') in txt:
                    actor_context = False
                    desc_context = True
                else:
                    if actor_context:
                        actor = actor + txt.decode('utf-8') + '\n'
                    elif desc_context:
                        desc = desc + txt.decode('utf-8') + '\n'

            desc_context = False
            item['actor'] = actor
            item['desc'] = desc
            # item['magnet'] = magnets.extract()
            yield item
        else:
            return
