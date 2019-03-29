# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class MetaItem(Item):
    collection = 'video_meta'

    vid = Field()
    video_url = Field()
    image_url = Field()
    video_type = Field()
    cid = Field()
    create = Field()

class VideoItem(Item):
    collection = 'video_detail'
    vid = Field()
    video_name = Field()
    play_count=Field()
    up_name = Field()
    up_id = Field()
    time_length = Field()
    danmu = Field()
    like=Field()
    dislike=Field()
    tid = Field()
    tag = Field()

class CommentItem(Item):

    vid=Field()
    content=Field()






