import json
from datetime import datetime

import pandas as pd

from banker.banker import Banker
from config.logger import get_logger
from gambler.gamble_record import GambleRecord
from util.util import Util


class Gambler(object):
    """
    Gambling instance

    Args:
        target (dict): filter to get gamble info from banker, leave blank for all.
    """

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

    def battle(self, start_date, end_date=None, **target):
        end_date = end_date or Util.get_last_game()["game_time"][:10]
        self.logger.debug(
            f"gambler_{self.gambler_id} start battle, {start_date} to {end_date}"
        )

        for game_date in pd.date_range(
            datetime.strptime(start_date, "%Y%m%d"),
            datetime.strptime(end_date, "%Y-%m-%d"),
        ):
            game_date = game_date.strftime("%Y%m%d")
            gamble_info = Banker().get_gamble_info(game_date=game_date, **target)

            # [decision, decision, ...]
            decisions = self.strategy_provider.get_decisions(self, gamble_info)
            self.decision_history += decisions
            records = self.settle(decisions)
            self.write_records(records)

        self.logger.debug(f"gambler {self.gambler_id} finished battle.")

    def settle(self, decisions):
        self.logger.debug("start settle")
        records = []
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
                try:
                    response_ratio = gamble_info.handicap[decision.bet.banker_side][
                        decision.bet.type
                    ]["response"][decision.bet.result]
                except KeyError as e:
                    self.logger.error(f"unable to get response ratio: {e}")
                    raise e
                self.principle += decision.bet.unit * response_ratio
            else:
                decision.match = False

            self.logger.debug("settled decision: %s" % decision)
            self.logger.debug("current principle: %s" % self.principle)
            record.content["principle"]["after"] = self.principle
            records.append(record)
        return records

    def write_records(self, records):
        self.logger.debug(f"save decision to mongodb: {records}")
        for record in records:
            doc = json.loads(json.dumps(record.content, default=lambda o: o.__dict__))
            self.mongo_client.update(doc, doc, upsert=True)
