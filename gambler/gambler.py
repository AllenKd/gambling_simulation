import json
from datetime import datetime

import pandas as pd

from banker.banker import Banker
from config.logger import get_logger
from gambler.gamble_record import GambleRecord
from util.util import Util


class Gambler(object):
    def __init__(self, gambler_id, principle, strategy_provider):
        self.logger = get_logger("gambler_{}".format(gambler_id))
        self.gambler_id = gambler_id
        self.principle = principle
        self.config = Util().get_config()

        self.strategy_provider = strategy_provider
        self.decision_history = []
        self.mongo_client = Util.get_mongo_client()["gambling_simulation"][
            "battle_data"
        ]

    # TODO: end_date should be end of the gamble
    def battle(self, start_date, end_date=datetime.today().strftime("%Y%m%d")):
        for game_date in pd.date_range(
            datetime.strptime(start_date, "%Y%m%d"),
            datetime.strptime(end_date, "%Y%m%d"),
        ):
            game_date = game_date.strftime("%Y%m%d")
            gamble_info = Banker().get_gamble_info(game_date=game_date)

            # [decision, decision, ...]
            decisions = self.strategy_provider.get_decision(self, gamble_info)
            self.decision_history += decisions
            self.settle(decisions)

    def settle(self, decisions):
        self.logger.debug("start settle")
        for decision in decisions:
            self.logger.debug(f"settling decision: {decision}")
            record = GambleRecord(self.gambler_id, self.strategy_provider)
            gamble_result = Banker().get_gamble_result(
                decision.game_date, decision.gamble_id
            )
            record.content["decision"] = decision
            record.content["principle"] = {"before": self.principle}
            self.principle -= decision.bet.unit
            if (
                decision.bet.result
                == gamble_result.judgement[decision.bet.banker_side][decision.bet.type]
            ):
                decision.match = True
                gamble_info = Banker().get_gamble_info(
                    game_date=decision.game_date, gamble_id=decision.gamble_id
                )[0]
                response_ratio = gamble_info.handicap[decision.bet.banker_side][
                    decision.bet.type
                ]["response"][decision.bet.result]
                self.principle += decision.bet.unit * response_ratio
            else:
                decision.match = False

            self.logger.debug("settled decision: %s" % decision)
            self.logger.debug("current principle: %s" % self.principle)
            record.content["principle"]["after"] = self.principle
            self.write_record(record)

    def write_record(self, record):
        self.logger.debug(f"save decision to mongodb: {record}")
        doc = json.loads(json.dumps(record.content, default=lambda o: o.__dict__))
        self.mongo_client.update(doc, doc, upsert=True)
