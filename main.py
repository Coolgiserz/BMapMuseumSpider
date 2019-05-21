__author__='CoolCats'

from scrapy.cmdline import execute
import sys
import os
print(os.path.dirname(os.path.abspath(__file__)))
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)
execute(["scrapy","crawl","bmuseum"])