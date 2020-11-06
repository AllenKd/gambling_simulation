import logging
from datetime import datetime
from functools import lru_cache

from banker.objects import GambleInfo, GambleResult
from db.collection.sports_data import SportsData
from util.singleton import Singleton
from strategy_provider.common.decision import Decision


class Banker(metaclass=Singleton):
    @lru_cache(1024)
    def get_gamble_info(self, game_date, **kwargs) -> [GambleInfo]:
        logging.debug(f"getting gamble info, game date: {game_date}")
        game_date = str(datetime.strptime(game_date, "%Y%m%d").date())
        a = SportsData.objects(
            timestamp__data=datetime.strptime(game_date, "%Y%m%d").date()
        )
        query_condition = {"game_time": {"$regex": game_date}}
        query_condition.update(**kwargs)
        return [GambleInfo(i) for i in a]

    @lru_cache(1024)
    def _get_gamble_result(
        self, game_time: datetime, gamble_id: str, game_type: str
    ) -> SportsData:
        return SportsData.objects(
            gamble_id=gamble_id, game_type=game_type, game_time=game_time,
        )

    def check(self, decision: Decision) -> bool:
        sports_data = self._get_gamble_result(
            decision.game_time, decision.gamble_id, decision.game_type
        )
        gamble_info = getattr(sports_data.gamble_info, decision.game_type)
        return gamble_info.judgement == decision.bet.result
