# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyzhihunewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ZhihuUserItem(scrapy.Item):
    url_token = scrapy.Field()  ##知乎分配的唯一用户ID
    url = scrapy.Field()   ###用户的url
    name = scrapy.Field()  ###姓名
    answer_count = scrapy.Field()  ##回答数量
    articles_count = scrapy.Field()  ###文章数量
    description = scrapy.Field()    ###自己描述
    follower_count = scrapy.Field()  ###关注者
    following_count = scrapy.Field() ###关注了
    headline = scrapy.Field()  ####职业
    voteup_count = scrapy.Field()   ##获得的赞数
    favorited_count = scrapy.Field()  ##被收藏次数
    thanked_count = scrapy.Field()  ###被感谢次数

    def get_insert_sql(self):
        insert_sql = """
               insert into zhihu_user_info(url_token, url, name, answer_count, articles_count,description,follower_count,following_count,
              headline, voteup_count,favorited_count,thanked_count
               )
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s, %s,%s) ON DUPLICATE KEY UPDATE 
               answer_count=VALUES(answer_count), description=VALUES(description), follower_count=VALUES(follower_count), 
               voteup_count=VALUES(voteup_count), favorited_count=VALUES(favorited_count),thanked_count=VALUES(thanked_count),
               articles_count=VALUES(articles_count),following_count=VALUES(following_count)
           """
        params = (self['url_token'],"https://www.zhihu.com/people/"+str(self['url_token']),self['name'],self['answer_count'],self['articles_count'],
                self['description'],self['follower_count'],self['following_count'],self['headline'],self['voteup_count'],self['favorited_count'],self['thanked_count'])

        return insert_sql, params









