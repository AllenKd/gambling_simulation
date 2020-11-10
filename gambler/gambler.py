import logging

from mongoengine.errors import DoesNotExist

from banker.banker import Banker
from banker.objects import GambleInfo
from db.collection.gambler import Gambler as GamblerCollection
from gambler.document_builder import parse_decision
from strategy_provider.common.decision import Decision
from util.util import Util


class Gambler:
    def __init__(self, name, capital, strategy):
        self.name = name
        self.capital = capital
        self.config = Util().get_config()

        self.strategy = strategy
        self.decision_history = []

        logging.debug(f"gambler initialized: ", name)

    def play(self, gamble_info: [GambleInfo]):
        logging.debug(f"[{self.name}] start battle: {gamble_info[0].game_time}")

        decisions = self.strategy.bet.get_decisions(self, gamble_info)
        for decision in decisions:
            self.battle(decision)

        logging.debug(f"[{self.name}] finish battle: {gamble_info[0].game_time}")

    def battle(self, decision: Decision):
        try:
            decision.match = Banker().check(decision)
            battle_history = parse_decision(decision)
            battle_history.capital_before = self.capital
            battle_history.capital_after = self.capital - decision.bet.unit + (
                    decision.match * decision.bet.unit * decision.get_response())
            GamblerCollection.objects.get(name=self.name).battle_history.append(battle_history)
            GamblerCollection.save()

        except DoesNotExist as e:
            logging.error(f"fail to check decision: {e}")

        except Exception as e:
            logging.error(e)
