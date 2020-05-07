import os
from functools import lru_cache

import pymysql
import yaml
from pymongo import MongoClient
from sqlalchemy import create_engine

from config.logger import get_logger
from util.singleton import Singleton


class Util(metaclass=Singleton):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        with open("config/configuration.yml", "r") as config:
            self.config = yaml.load(config, Loader=yaml.Loader)

    def load_environment_variable(self):
        self.logger.info("start load environment variables and overwrite config file")
        with open("config/configuration.yml") as config:
            config = yaml.load(config, Loader=yaml.FullLoader)

            config["DB"]["host"] = os.environ.get("DB_HOST") or config["DB"]["host"]

            config["DB"]["port"] = (
                int(os.environ.get("DB_PORT"))
                if os.environ.get("DB_PORT")
                else config["DB"]["port"]
            )

            config["DB"]["user"] = os.environ.get("DB_USERNAME") or config["DB"]["user"]

            config["DB"]["password"] = (
                os.environ.get("DB_PASSWORD") or config["DB"]["password"]
            )

        # overwrite config by environment variable
        with open("config/configuration.yml", "w") as new_config:
            yaml.dump(config, new_config)

        self.config = config
        self.logger.debug("finish update config file")
        return

    @lru_cache(1)
    def get_config(self):
        self.logger.info("getting config")
        return self.config

    def get_db_connection(self):
        self.logger.info("getting db connection")
        user = self.config["DB"]["user"]
        password = self.config["DB"]["password"]
        host = self.config["DB"]["host"]
        port = self.config["DB"]["port"]
        return pymysql.connect(
            host=host,
            user=user,
            passwd=password,
            port=port,
            db=self.config["DB"]["schema"],
            charset="utf8",
        )

    @classmethod
    def get_mongo_client(cls):
        return MongoClient(
            host=Util().config["mongoDb"]["host"],
            port=Util().config["mongoDb"]["port"],
            username=Util().config["mongoDb"]["username"],
            password=Util().config["mongoDb"]["password"],
            authMechanism="SCRAM-SHA-1",
        )

    @classmethod
    def get_last_game(cls):
        return Util.get_mongo_client()["gambling_simulation"]["sports_data"].find_one(
            {}, sort=[("game_time", -1)]
        )

    def get_db_engine(self):
        self.logger.info("getting db engine")
        user = self.config["DB"]["user"]
        password = self.config["DB"]["password"]
        host = self.config["DB"]["host"]
        port = self.config["DB"]["port"]
        return create_engine(
            "mysql+pymysql://{}:{}@{}:{}".format(user, password, host, port)
        )

    @classmethod
    def confidence_to_prob(cls, confidence):
        # confidence index with 95% less than 6000
        return min(confidence / 6000, 1)
