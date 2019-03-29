# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import Bzhan.settings
import pymysql
import time
from Bzhan.items import *
from Bzhan.settings import *

pymysql.install_as_MySQLdb()




class MySQLPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=Mysql_host,
            db=Mysql_db,
            user=Mysql_user,
            passwd=Mysql_password,
            charset='utf8',
            port=MYSQL_PORT,
            use_unicode=True
        )

        self.cursor = self.connect.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

    def process_item(self, item, spider):
        if isinstance(item, MetaItem):
            try:
                self.cursor.execute(
                    "insert into " + item.collection + "(vid, video_url, image_url, video_type,cid,create_time)\
                      value (%d, '%s', '%s', %d, %d,'%s')"%(item['vid'],
                     item['video_url'],
                     item['image_url'],
                     item['video_type'],
                     item['cid'],
                     item['create']))
                self.connect.commit()
            except Exception as error:
                spider.logger.info(error)
        elif isinstance(item, VideoItem):
            try:
                self.cursor.execute(
                    "insert into "+item.collection+"(vid, video_name, play_count ,up_name,up_id, time_length, danmu, like_count, dislike_count, tid, tag) value (%d,'%s',%d,'%s',%d, %d, '%s', %d, %d, %d ,'%s')"%(
                     item['vid'],
                     item['video_name'],
                     item['play_count'],
                     item['up_name'],
                     item['up_id'],
                     item['time_length'],
                     item['danmu'],
                     item['like'],
                     item['dislike'],
                     item['tid'],
                     item['tag']
                     )
                    )
                self.connect.commit()
            except Exception as error:
                spider.logger.info(error)
        return item