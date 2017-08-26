# -*- coding: utf-8 -*-

import MySQLdb
import logging
import traceback


def singleton(cls, *args, **kw):
    instance = {}

    def _singleton():
        if cls not in instance:
            instance[cls] = cls(*args, **kw)
        return instance[cls]

    return _singleton


@singleton
class MySQLItemDao(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host='192.168.2.66',
                                    user='scrapy',
                                    passwd='8w9oMXpHHezwKFqP',
                                    db='scrapy')
        self.log = logging.getLogger(__name__)
        self.log.info("mysql connected")

    def new_movie(self, item):
        cursor = self.conn.cursor()
        poster = u''
        for p in item['mv_poster']:
            poster = poster+p+u','

        sql = u"""INSERT INTO scrapy.`movie_info` 
               (`mv_name`,
               `mv_name_trans`,
               `mv_period`,
               `mv_lang`, 
               `mv_region`, 
               `mv_imdb_score`, 
               `mv_imdb_url`, 
               `mv_douban_score`, 
               `mv_douban_url`, 
               `mv_length`, 
               `mv_director`, 
               `mv_actor`, 
               `mv_poster`,
               `mv_desc`,
               `url`)
        VALUES ('{name_zh}',
                '{name_en}',
                '{period}', 
                '{lang}', 
                '{region}', 
                '{imdb_s}', 
                '{imdb_url}', 
                '{douban_s}', 
                '{douban_url}', 
                '{mv_length}', 
                '{director}', 
                '{actor}', 
                '{mv_poster}',
                '{desc}',
                '{url}')""".format(
            name_zh=item['name_zh'],
            name_en=item['name_en'],
            period=item['period'],
            lang=item['lang'],
            region=item['region'],
            imdb_s=item['imdb_s'],
            imdb_url=item['imdb_url'],
            douban_s=item['douban_s'],
            douban_url=item['douban_url'],
            mv_length=item['mv_length'],
            director=item['director'],
            actor=item['actor'],
            mv_poster=poster[:-1],
            desc=item['desc'],
            url=item['url']
        )
        try:
            if cursor.execute(sql):
                return cursor.lastrowid
            else:
                return 0L
            self.log.error(args)
        except BaseException, args:
            traceback.print_exc()
            self.conn.rollback()
        finally:
            self.conn.commit()
            cursor.close()

    def new_movie_type_link(self, movie_id, mv_class):
        try:
            cursor = self.conn.cursor()
            select_sql = u"select type_id from scrapy.`movie_type` where `type_name`='%s'" % mv_class

            if cursor.execute(select_sql):
                type_id = cursor.fetchone()[0]
            else:
                insert_sql = u"insert into scrapy.`movie_type`(`type_name`) values('%s')" % mv_class
                cursor.execute(insert_sql)
                type_id = int(cursor.lastrowid)
            sql = u"insert into scrapy.`movie_type_link`(`movie_id`,`type_id`) values({},{})".format(movie_id, type_id)
            if cursor.execute(sql):
                return cursor.lastrowid
            else:
                return 0L
        except BaseException, args:
            self.log.error(args)
            traceback.print_exc()
            self.conn.rollback()
        finally:
            self.conn.commit()
            cursor.close()

        pass

    def new_movie_magnet(self, movie_id, magnet):
        sql = u"""insert into
                     scrapy.movie_download(`mv_id`,`resolution`,`name`,`url`)
                values
                     ({},{},'{}','{}')""".format(movie_id, magnet['resolution'], magnet['name'], magnet['url'])
        cursor = self.conn.cursor()
        try:
            if cursor.execute(sql):
                return cursor.lastrowid
            else:
                return 0L
        except BaseException, args:
            self.log.error(args)
            traceback.print_exc()
            self.conn.rollback()
        finally:
            self.conn.commit()
            cursor.close()

    def getCrawled(self):
        sql = "select distinct url from scrapy.`movie_info`"
        cursor = self.conn.cursor()
        try:
            if cursor.execute(sql):
                res = []
                for data in cursor.fetchall():
                    res.append(data[0])
                return res
            else:
                return []
        except BaseException,args:
            self.log.error(args)
            traceback.print_exc()
        finally:
            cursor.close()

    def close(self):
        self.conn.close()
        self.log.info("mysql connection closed")
