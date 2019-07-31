import datetime
import re
from collections import defaultdict

import pandas as pd
import requests
import yaml
import pymysql
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

from config.constant import crawler as crawler_constant
from config.constant import database as db_constant
from config.constant import global_constant
from config.logger import get_logger


class DataUpdater(object):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        with open('config/configuration.yml') as config:
            self.config = yaml.load(config, Loader=yaml.FullLoader)

            # create db connection
            user = self.config[global_constant.DB][global_constant.user]
            password = self.config[global_constant.DB][global_constant.password]
            host = self.config[global_constant.DB][global_constant.host]
            port = self.config[global_constant.DB][global_constant.port]
            self.db = pymysql.connect(host=host, user=user, passwd=password, port=port,
                                      db=self.config[global_constant.DB][global_constant.schema], charset='utf8')

    def update_db(self):
        pass

    def get_latest_record(self):
        pass
