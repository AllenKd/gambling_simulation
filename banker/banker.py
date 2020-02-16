from datetime import datetime
from functools import lru_cache

from pymongo import MongoClient

from banker.objects import GambleInfo, GambleResult
from config.logger import get_logger
from utility.utility import Utility


# should be singleton
class Banker:
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.config = Utility().get_config()
        # self.game_result = np.random.randint(2, size=play_times * combination).reshape(play_times, combination)
        self.mongo_client = MongoClient(host=self.config['mongoDb']['host'],
                                        port=self.config['mongoDb']['port'])['gambling_simulation']['sports_data']

    @lru_cache(16)
    def get_gamble_info(self, game_date, **kwargs):
        self.logger.debug('getting gamble info, game date: %s' % game_date)
        game_date = str(datetime.strptime(game_date, '%Y%m%d').date())
        query_condition = {'game_time': {'$regex': game_date}}
        query_condition.update(**kwargs)
        return [GambleInfo(i) for i in self.mongo_client.find(query_condition)]

    @lru_cache(64)
    def get_gamble_result(self, game_date, gamble_id):
        game_date = str(datetime.strptime(game_date, '%Y%m%d').date())
        query_condition = {'game_time': {'$regex': game_date}, 'gamble_id': gamble_id}
        return [GambleResult(i) for i in self.mongo_client.find(query_condition)]
