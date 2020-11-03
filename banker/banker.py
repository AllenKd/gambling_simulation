from datetime import datetime
from functools import lru_cache

from banker.objects import GambleInfo, GambleResult
from config.logger import get_logger
from util.singleton import Singleton
from db.collection.sports_data import SportsData
from util.util import Util
import logging


class Banker(metaclass=Singleton):

    @lru_cache(1024)
    def get_gamble_info(self, game_date, **kwargs):
        logging.debug(f"getting gamble info, game date: {game_date}")
        game_date = str(datetime.strptime(game_date, "%Y%m%d").date())
        a = SportsData.objects(timestamp__data=datetime.strptime(game_date, "%Y%m%d").date())
        query_condition = {"game_time": {"$regex": game_date}}
        query_condition.update(**kwargs)
        return [GambleInfo(i) for i in a]

    @lru_cache(1024)
    def get_gamble_result(self, game_date, gamble_id):
        game_date = str(datetime.strptime(game_date, "%Y%m%d").date())
        query_condition = {"game_time": {"$regex": game_date}, "gamble_id": gamble_id}
        a = SportsData.objects(timestamp__data=datetime.strptime(game_date, "%Y%m%d").date(), gamble_id=gamble_id)
        # query_result = self.mongo_client.find_one(query_condition)
        # self.logger.debug("query result: %s" % query_result)
        return GambleResult(a)
