import logging
import datetime
from functools import lru_cache

from banker.objects import GambleInfo
from db.collection.sports_data import SportsData
from strategy_provider.common.decision import Decision
from util.singleton import Singleton
from datetime import datetime
from mongoengine import Q


class Banker(metaclass=Singleton):
    @lru_cache(1024)
    def get_gamble_info(self, game_date: datetime.date, **kwargs) -> [GambleInfo]:
        logging.debug(f"getting gamble info, game date: {game_date}")
        # game_date = str(datetime.strptime(game_date, "%Y%m%d").date())
        a = SportsData.objects(
            Q(game_time__gte=game_date) & Q(game_time__lte=game_date + datetime.timedelta(days=1))
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
