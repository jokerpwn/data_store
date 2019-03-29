import json
from scrapy import Request, Spider
import requests
import re
from Bzhan.items import *

class BzhanSpider(Spider):
    name = 'Bzhancn'

    music_list = [28, 31, 30, 194, 59, 29, 54, 130]

    meta_url = 'https://api.bilibili.com/archive_rank/getarchiverankbypartion?jsonp=jsonp&tid={tid}&pn={page}'
    detail_url = 'https://api.bilibili.com/x/web-interface/view?aid={vid}'
    comment_url= 'https://api.bilibili.com/x/v2/reply?type=1&sort=2&oid={vid}&pn={page}&nohot=1'
    rank_url = 'https://api.bilibili.com/x/web-interface/ranking?rid=3&day={day}&jsonp=jsonp'
    vedio_url='https://www.bilibili.com/video/av{vid}'
    danmu_url='https://comment.bilibili.com/{vid}.xml'

    def start_requests(self):
        for tid in self.music_list:
            yield Request(self.meta_url.format(tid=tid,page=1), callback=self.parse_meta,
                          meta={'tid':tid,'page':1})

    def parse_meta(self, response):
        """

        :param response:
        :return:
        """
        tid=response.meta.get('tid')
        #self.logger.debug(response)
        result = json.loads(response.text)
        if result.get('code')==0 and result.get('data').get('archives'):
            meta_info = result.get('data').get('archives')

            for video in meta_info:
                mete_item = MetaItem()

                mete_item['vid'] = video.get('aid')
                mete_item['video_url']=self.vedio_url.format(vid=video['aid'])
                mete_item['image_url']= video.get('pic')
                mete_item['video_type']=video.get('tid')
                mete_item['cid']=video.get('cid')
                mete_item['create']=video.get('create')
                yield mete_item
                #读视频信息
                yield Request(self.detail_url.format(vid=video['aid']),callback=self.parse_detail,
                              meta={'tid':tid})


            page = response.meta.get('page') + 1
            # 下一页
            yield Request(self.meta_url.format(tid=tid,page=page), callback=self.parse_meta,
                          meta={'page':page ,'tid':tid})

    def parse_detail(self, response):

        result = json.loads(response.text)

        if result.get('code')==0 and result.get('data'):
            # 解析视频
            detail_info=result['data']
            detail_item=VideoItem()
            detail_item['vid']=detail_info.get('aid')
            detail_item['video_name']=detail_info.get('title')
            detail_item['video_name'] = detail_item['video_name'].replace("\\", "\\\\")
            detail_item['video_name']=detail_item['video_name'].replace("'","\\'")
            detail_item['video_name'] = detail_item['video_name'].replace('"', '\\"')

            detail_item['play_count'] = detail_info.get('stat').get('view')
            detail_item['up_name'] = detail_info.get('owner').get('name')
            detail_item['up_id']=detail_info.get('owner').get('mid')
            detail_item['time_length'] = detail_info.get('duration')
            detail_item['like'] = detail_info.get('stat').get('like')
            detail_item['dislike'] = detail_info.get('stat').get('dislike')
            detail_item['tid']=detail_info.get('tid')
          
            detail_item['tag'] = detail_info.get('dynamic')
            # 读弹幕信息
            danmu_response=requests.get(self.danmu_url.format(vid=detail_item['vid']))

            str="\n".join(re.findall(r'<d.*?>(.*?)</d>', danmu_response.text))
            str = str.replace("\\", "\\\\")
            str=str.replace("'","\\'")
            str=str.replace('"', '\\"')

            detail_item['danmu'] = str
            yield detail_item

    # def parse_comment(self, response):
    #     result = json.loads(response.text)
    #     if result.get('data'):
    #         # 读评论信息
    #         comment = CommentItem()
    #         comment_response = requests.get(self.comment_url.format(vid=detail_item['vid'], page=1))
    #         comment_info = json.loads(comment_response.text)
    #         page = comment_info.get('page')
    #
    #         for p in range(1, page['count'] / page['size']):
