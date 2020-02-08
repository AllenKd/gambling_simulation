import pandas as pd
import yaml

from config.constant import player as player_constant
from config.constant import strategy_provider as sp_constant
from config.logger import get_logger


class Player(object):
    def __init__(self, player_id, strategy_provider, bet_strategy):
        self.id = player_id
        self.logger = get_logger('player{}'.format(self.id))
        with open('config/configuration.yml', 'r') as config:
            self.config = yaml.load(config, Loader=yaml.FullLoader)

        self.bet_strategy = bet_strategy
        self.strategy_provider = strategy_provider
        self.battle_history = pd.DataFrame(columns=player_constant.battle_target)

    def battle(self, game_judgement):
        self.logger.info('start battle'.format(self.id))
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
