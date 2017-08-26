# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from gq.items import GqItem
from gq.item_dao import MySQLItemDao


class GaoqingSpider(CrawlSpider):
    name = 'gaoqing'
    allowed_domains = ['gaoqing.la']
    start_urls = ['http://gaoqing.la/']

    rules = (
        Rule(LinkExtractor(allow=r'.*\.html'),
             callback='parse_item', follow=True),
    )
    

    def parse_item(self, response):

        self.crawled=MySQLItemDao().getCrawled()
        if response.url in self.crawled:
            return
        title = response.xpath('//title/text()').extract()[0]

        magnets = response.xpath('//a[contains(@href,"magnet")]')
        if len(magnets) > 0:
            self.logger.info(u'url:[{0}],name:[{1}]'.format(response.url, title))

            content = response.xpath('//*[@id="post_content"]')
            item = GqItem()
            # item['magnet'] = magnets.extract()
            item['mv_poster'] = content.xpath('./p//img/@src').extract()
            actor_context = False
            desc_context = False
            actor = u''
            desc = u''
            for txt in content.xpath('./p/span//text()').extract():
                try:
                    txt = txt.encode('utf-8').replace('　', '')
                    if '译名' in txt or '又名' in txt:
                        item['name_en'] = txt[9:].decode('utf-8')
                    elif '片名' in txt:
                        item['name_zh'] = txt[9:].decode('utf-8')
                    elif '年代' in txt:
                        item['period'] = int(txt[9:])
                    elif '产地' in txt or '国家' in txt:
                        item['region'] = txt[9:].decode('utf-8')
                    elif '类别' in txt:
                        item['mv_class'] = txt[9:].replace('/', ',').decode('utf-8')
                    elif '语言' in txt:
                        item['lang'] = txt[9:].decode('utf-8')
                    elif '上映日期' in txt:
                        item['uptime'] = txt[15:].decode('utf-8')
                    elif 'IMDb评分' in txt:
                        for i in range(4,40):
                            try:
                                txt2 = txt[i:]
                                score = int(float(txt2[:txt2.find('/')]) * 10)
                                item['imdb_s'] = score
                                break
                            except:
                                item['imdb_s'] = 0

                    elif 'IMDb链接' in txt:
                        item['imdb_url'] = txt[14:].decode('utf-8')
                    elif '豆瓣评分' in txt:
                        for i in range(4,40):
                            try:
                                txt2 = txt[i:]
                                score = int(float(txt2[:txt2.find('/')]) * 10)
                                item['douban_s'] = score
                                break
                            except:
                                item['douban_s'] = 0
                    elif '豆瓣链接' in txt:
                        item['douban_url'] = txt[15:].decode('utf-8')
                    elif '片长' in txt:
                        item['mv_length'] = int(re.findall(r'[0-9]*', txt[9:])[0])
                    elif '导演' in txt:
                        item['director'] = txt[9:].decode('utf-8')
                    elif '主演' in txt:
                        actor_context = True
                        actor = actor + txt[9:].decode('utf-8') + u','
                    elif '简介' in txt:
                        actor_context = False
                        desc_context = True
                    else:
                        if actor_context:
                            actor = actor + txt.decode('utf-8') + u','
                        elif desc_context:
                            desc = desc + txt.decode('utf-8')
                except BaseException,arg:
                    self.logger.warning(response.url)
                    self.logger.warning(arg)
                    continue

            item['actor'] = actor[:-1]
            item['desc'] = desc[:-1]
            magnetSet = []
            for m in magnets:
                magnet = {}
                magnet['name'] = m.xpath('.//text()').extract()[0]
                magnet['url'] = m.xpath('.//@href').extract()[0]
                resolution = 1080
                if u'720' in magnet['name']:
                    resolution = 720
                magnet['resolution'] = resolution
                magnetSet.append(magnet)
            item['magnet'] = magnetSet
            item['url'] = response.url
            if 'name_zh' not in item:
                item['name_zh'] = title
            if 'name_en' not in item:
                item['name_en'] = item['name_zh']

            yield item
        else:
            return

    def close(self, reason):
        MySQLItemDao().close()
        self.logger.info('FUCK_FUCK_FUCK_FUCK!')
    
