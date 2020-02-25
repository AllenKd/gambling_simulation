from datetime import datetime

import pandas as pd

from banker.banker import Banker
from config.constant import strategy_provider as sp_constant
from config.logger import get_logger
from utility.utility import Utility


class Gambler(object):
    def __init__(self, gambler_id, principle, strategy_provider):
        self.logger = get_logger('gambler_{}'.format(gambler_id))
        self.gambler_id = gambler_id
        self.principle = principle
        self.config = Utility().get_config()

        self.strategy_provider = strategy_provider
        self.decision_history = []

    def battle(self, start_date, end_date=datetime.today().strftime('%Y%m%d')):
        for game_date in pd.date_range(datetime.strptime(start_date, '%Y%m%d'), datetime.strptime(end_date, '%Y%m%d')):
            game_date = game_date.strftime('%Y%m%d')
            gamble_info = Banker().get_gamble_info(game_date=game_date)

            # [decision, decision, ...]
            decisions = self.strategy_provider.get_decision(self, gamble_info)
            self.decision_history += decisions
            self.settle(decisions)

    def settle(self, decisions):
        self.logger.debug('start settle')
        for decision in decisions:
            gamble_result = Banker().get_gamble_result(decision.game_date, decision.gamble_id)
            for bet in decision.bets:
                self.principle -= bet.unit
                if bet.result == gamble_result.judgement[bet.banker_side][bet.type]:
                    decision.match = True
                    gamble_info = Banker().get_gamble_info(game_date=decision.game_date,
                                                           gamble_id=decision.gamble_id)[0]
                    response_ratio = gamble_info.handicap[bet.banker_side][bet.type].get('response', 1.7)
                    self.principle += bet.unit * response_ratio
                else:
                    decision.match = False

            self.logger.debug('settled decision: %s' % decision)
            self.logger.debug('current principle: %s' % self.principle)

    def summarize_battle_history(self):
        self.logger.debug('start summarize battle history')
        full_strategy_name = self.bet_strategy.name if self.bet_strategy.name != sp_constant.low_of_large \
            else '{}_{}'.format(self.bet_strategy.name, self.bet_strategy.kwargs['recency'])

        return pd.Series([full_strategy_name]).append(self.decision_history.mean().round(3)).values
