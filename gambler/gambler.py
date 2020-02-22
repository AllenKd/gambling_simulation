import pandas as pd

from banker.banker import Banker
from config.constant import strategy_provider as sp_constant
from config.logger import get_logger
from utility.utility import Utility


class Gambler(object):
    def __init__(self, gambler_id, principle, strategy_provider):
        self.logger = get_logger('gambler_{}'.format(self.gambler_id))
        self.gambler_id = gambler_id
        self.principle = principle
        self.config = Utility.get_config()

        self.strategy_provider = strategy_provider
        self.battle_history = pd.DataFrame(columns=player_constant.battle_target)

    def n_battle(self, start_date):
        gamble_info = Banker().get_gamble_info(game_date=start_date)

        # [decision, decision, ...]
        decisions = self.strategy_provider.get_decision(self, gamble_info)
        self.settle(decisions)

    def settle(self, decisions):
        self.logger.debug('start settle')
        for decision in decisions:
            game_result = Banker().get_gamble_result(decision.gamble_id)
            for banker_side in decision:
                for bet_type, bet_decision in banker_side.items():
                    self.logger.debug('settle game: %s' % decision)
                    if bet_decision[0] == game_result[banker_side][bet_type]:
                        decision.match = True
                        gamble_info = Banker().get_gamble_info(game_date=decision.game_date,
                                                               gamble_id=decision.gamble_id)
                        response_ratio = gamble_info.handicap[banker_side][bet_type].get('response', 1.7)
                        self.principle += bet_decision[1] * response_ratio
                    else:
                        decision.match = False
                        self.principle -= bet_decision[1]

    def battle(self, game_judgement):
        self.logger.info('start battle'.format(self.gambler_id))
        for row_id, game_result in game_judgement.iterrows():
            kwargs = self.bet_strategy_kwargs(game_judgement, row_id)
            bet = self.strategy_provider.get_bet_decision(self.bet_strategy, **kwargs)
            battle_result = bet == game_result
            self.battle_history.loc[row_id] = battle_result.astype(int)
        self.logger.debug('finished battle, runs: {}'.format(len(self.battle_history)))
        return self.battle_history

    def bet_strategy_kwargs(self, game_judgement, row_id):
        self.logger.debug('start generate ber strategy kwargs')
        if self.bet_strategy.name == sp_constant.low_of_large:
            return {'game_history': game_judgement[game_judgement.index < row_id]}
        return dict()

    def summarize_battle_history(self):
        self.logger.debug('start summarize battle history')
        full_strategy_name = self.bet_strategy.name if self.bet_strategy.name != sp_constant.low_of_large \
            else '{}_{}'.format(self.bet_strategy.name, self.bet_strategy.kwargs['recency'])

        return pd.Series([full_strategy_name]).append(self.battle_history.mean().round(3)).values
