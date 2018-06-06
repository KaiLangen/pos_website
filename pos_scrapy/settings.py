# -*- coding: utf-8 -*-

import random
from pos_scrapy.helpers import *

BOT_NAME = 'pos_scrapy'

SPIDER_MODULES = ['pos_scrapy.spiders']
NEWSPIDER_MODULE = 'pos_scrapy.spiders'

USER_AGENT = random.choice(USER_AGENTS)

ITEM_PIPELINES = {
    'pos_scrapy.pipelines.PosScrapyPipeline': 0, }

DOWNLOAD_DELAY = 0.98765
RANDOMIZE_DOWNLOAD_DELAY = True
CONCURRENT_REQUESTS_PER_IP = 1
CONCURRENT_REQUESTS = 1
CONCURRENT_ITEMS = 10

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = False
AUTOTHROTTLE_START_DELAY = 1.2345

LOG_ENABLED = True
LOG_LEVEL = "DEBUG"
LOG_FILE = False  # 'debug_output.txt'
LOG_STDOUT = True
LOG_DATEFORMAT = '%d-%m-%y %H:%M:%S'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'

TELNETCONSOLE_ENABLED = False

PROCESS_CSV = True
CSV_PATH = 'D:\\Dropbox\\Work\\Upwork\\posproject\\pos_website\\csv\\'
