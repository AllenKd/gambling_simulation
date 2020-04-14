from datetime import datetime
from functools import lru_cache

from banker.objects import GambleInfo, GambleResult
from config.logger import get_logger
from util.singleton import Singleton
from util.util import Util


# should be singleton
class Banker(metaclass=Singleton):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.config = Util().get_config()
        # self.game_result = np.random.randint(2, size=play_times * combination).reshape(play_times, combination)
        self.mongo_client = Util.get_mongo_client()["gambling_simulation"][
            "sports_data"
        ]

    @lru_cache(1024)
    def get_gamble_info(self, game_date, **kwargs):
        self.logger.debug("getting gamble info, game date: %s" % game_date)
        game_date = str(datetime.strptime(game_date, "%Y%m%d").date())
        query_condition = {"game_time": {"$regex": game_date}}
        query_condition.update(**kwargs)
        return [GambleInfo(i) for i in self.mongo_client.find(query_condition)]

    @lru_cache(1024)
    def get_gamble_result(self, game_date, gamble_id):
        game_date = str(datetime.strptime(game_date, "%Y%m%d").date())
        query_condition = {"game_time": {"$regex": game_date}, "gamble_id": gamble_id}
        query_result = self.mongo_client.find_one(query_condition)
        self.logger.debug("query result: %s" % query_result)
        return GambleResult(query_result)
