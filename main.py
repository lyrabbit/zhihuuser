#_*_ coding:utf-8_*_
from scrapy.cmdline import execute

import sys
import os
##将爬虫项目根路径加到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__name__)))

execute(['scrapy','crawl','zhihu'])

