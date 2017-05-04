# -*- coding: utf-8 -*-

import scrapy
import re
import json
import requests
import urllib2
from ScrapyZhihuNew.items import ZhihuUserItem
from scrapy.contrib.loader import ItemLoader

class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['http://www.zhihu.com/']
    start_user = 'wang-tuan-jie-55'  ##开始爬取的第一个用户的ID
    ##获取用户信息需要的参数
    get_info_attr = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    ###获取他关注的人和关注他的人需要的参数
    get_follow_attr = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    ###获取他关注的人的
    get_followees = 'https://www.zhihu.com/api/v4/members/{user_name}/followees?include={include_info}&offset={offset}&limit={limit}'

    ####获取关注他的人 粉丝
    get_followers = 'https://www.zhihu.com/api/v4/members/{user_name}/followers?include={include_info}&offset={offset}&limit={limit}'


    ###提取用户初始信息的初始url
    get_info_user = 'https://www.zhihu.com/api/v4/members/{user_name}?include={include_info}'

    def start_requests(self):
        print self.get_info_user.format(user_name=self.start_user,include_info=self.get_info_attr)
        yield scrapy.Request(url=self.get_info_user.format(user_name=self.start_user,include_info=self.get_info_attr),callback=self.get_userInformation)


    def get_userInformation(self,response):
        # item_loader = ItemLoader(item=ZhihuUserItem(),response=response)
        response_text = json.loads(response.text)
        item = ZhihuUserItem()
        for field in item.fields:
            if field in response_text:
                item[field] = response_text.get(field)   ##直接获取字典里面的值
        yield item
        yield scrapy.Request(url=self.get_followers.format(user_name=item['url_token'],include_info=self.get_follow_attr,offset=0,limit=20),callback=self.get_followersInfomation)
        yield scrapy.Request(url=self.get_followees.format(user_name=item['url_token'],include_info=self.get_follow_attr,offset=0,limit=20),callback=self.get_followeesInfomation)

    def get_followersInfomation(self,response):
        try:
            try:
               response_data = json.loads(response.text)
               for one_user in response_data['data']:
                   user_name = one_user['url_token']
                   yield scrapy.Request(url=self.get_info_user.format(user_name=user_name,include_info=self.get_info_attr),callback=self.get_userInformation)
               if 'paging' in response_data.keys() and response_data['paging'].get('is_end') ==False:
                   yield scrapy.Request(url=response_data['paging'].get('next'),callback=self.get_followersInfomation)
            except Exception as e:
                print u"该用户没有url_token或者数据"
        except Exception as e:
            print e,u"该用户没有粉丝"

    def get_followeesInfomation(self, response):
        try:
            try:
                response_data = json.loads(response.text)
                for one_user in response_data['data']:
                    user_name = one_user['url_token']
                    yield scrapy.Request(
                        url=self.get_info_user.format(user_name=user_name, include_info=self.get_info_attr),
                        callback=self.get_userInformation)
                if 'paging' in response_data.keys() and response_data['paging'].get('is_end') == False:
                    yield scrapy.Request(url=response_data['paging'].get('next'),
                                         callback=self.get_followeesInfomation)
            except Exception as e:
                print u"该用户没有url_token或者数据"
        except Exception as e:
            print e, u"该用户没有关注他人"















