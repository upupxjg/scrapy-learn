# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from gq.item_dao import MySQLItemDao
import logging


class ItemDefaultValue(object):
    def process_item(self, item, spider):
        if 'name_zh' not in item:
            item['name_zh'] = ''
        if 'name_en' not in item:
            item['name_en'] = ''
        if 'period' not in item:
            item['period'] = 2017
        if 'lang' not in item:
            item['lang'] = ''
        if 'region' not in item:
            item['region'] = ''
        if 'imdb_s' not in item:
            item['imdb_s'] = 0
        if 'imdb_url' not in item:
            item['imdb_url'] = ''
        if 'douban_s' not in item:
            item['douban_s'] = 0
        if 'mv_length' not in item:
            item['mv_length'] = 0
        if 'douban_url' not in item:
            item['douban_url'] = ''
        if 'director' not in item:
            item['director'] = ''
        if 'actor' not in item:
            item['actor'] = ''
        if 'mv_poster' not in item:
            item['mv_poster'] = []
        if 'desc' not in item:
            item['desc'] = ''
        if 'mv_class' not in item:
            item['mv_class'] = u'奇葩'

        return item


class GqPipeline(object):
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.dao = MySQLItemDao()

    def process_item(self, item, spider):

        mid = self.dao.new_movie(item)
        if mid:
            for mv_class in item['mv_class'].split(','):
                self.dao.new_movie_type_link(mid, mv_class)

            for magnet in item['magnet']:
                self.dao.new_movie_magnet(mid, magnet)
            self.log.debug("success save a film to db with id %d" % mid)
        else:
            self.log.error("save film to db failed!")
        return item
