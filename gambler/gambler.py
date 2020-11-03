import json
import logging
from datetime import datetime
from typing import List

import pandas as pd

from banker.banker import Banker
from banker.objects import GambleInfo
from gambler.gamble_record import GambleRecord
from util.util import Util


class Gambler(object):
    def __init__(self, name, capital, strategy_provider):
        self.name = name
        self.principle = capital
        self.config = Util().get_config()

        self.strategy_provider = strategy_provider
        self.decision_history = []

    def n_battle(self, gamble_info: List[GambleInfo]):
        logging.debug(f"[{self.name}] start battle: {gamble_info[0].game_date}")

        decisions = self.strategy_provider.get_decisions(self, gamble_info)
        self.decision_history += decisions
        records = self.settle(decisions)
        self.write_records(records)
        logging.debug(f"[{self.name}] finish battle: {gamble_info[0].game_date}")

    def battle(self, start_date, end_date=None, **target):
        logging.debug(f"gambler_{self.name} start battle, {start_date} to {end_date}")

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

        logging.debug(f"gambler {self.name} finished battle.")

    def settle(self, decisions):
        logging.debug("start settle")
        records = []
        for decision in decisions:
            logging.debug(f"settling decision: {decision}")
            record = GambleRecord(self.name, self.strategy_provider)
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
                    logging.error(f"unable to get response ratio: {e}")
                    raise e
                self.principle += decision.bet.unit * response_ratio
            else:
                decision.match = False

            logging.debug("settled decision: %s" % decision)
            logging.debug("current principle: %s" % self.principle)
            record.content["principle"]["after"] = self.principle
            records.append(record)
        return records

    def write_records(self, records):
        logging.debug(f"save decision to mongodb: {records}")
        for record in records:
            doc = json.loads(json.dumps(record.content, default=lambda o: o.__dict__))
            self.mongo_client.update(doc, doc, upsert=True)
