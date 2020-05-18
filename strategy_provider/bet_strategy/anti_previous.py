from strategy_provider.common.base_bet_strategy import BaseStrategy
from strategy_provider.common.decision import Bet
from strategy_provider.common.decision import Decision
from strategy_provider.bet_strategy.follow_previous import FollowPrevious


class AntiPrevious(BaseStrategy):
    """
    Strategy Description:
        Bet with anti side if the previous gamble.
    """

    def __init__(
        self,
        put_strategy,
        banker_side="local",
        game_type="NBA",
        bet_type="total_point",
        result="over",
    ):
        super().__init__("Anti Previous", put_strategy)
        self.banker_side = banker_side
        self.game_type = game_type
        self.bet_type = bet_type
        self.result = result

        self.anti_map = {
            "over": "under",
            "under": "over",
            "host": "guest",
            "guest": "host",
        }
        self.follow_previous = FollowPrevious(put_strategy=put_strategy)

    def get_decisions(self, gambler, gamble_info):
        self.logger.debug("get decision")
        decisions = self.follow_previous.get_decisions(gambler, gamble_info)
        assert len(decisions) == 1
        decisions[0].bet.result = self.anti_map[decisions[0].bet.result]
        return decisions
        # if gambler.decision_history:
        #     last_bet = gambler.decision_history[-1].bet
        # else:
        #     self.logger.debug("gambler has no decision history, make default decision")
        #     last_bet = Bet(
        #         banker_side=self.banker_side,
        #         bet_type=self.bet_type,
        #         result=self.result,
        #         unit=1,
        #     )
        #
        # decisions = []
        # for info in gamble_info:
        #     if info.game_type == self.game_type:
        #         last_bet.result = self.anti_map[last_bet.result]
        #         decision = Decision(
        #             game_type=self.game_type,
        #             game_date=info.game_date,
        #             gamble_id=info.gamble_id,
        #             bet=last_bet,
        #         )
        #         decision.bet.unit = self.put_strategy.get_unit(
        #             info, decision, gambler, self
        #         )
        #         if decision.bet.unit:
        #             decisions.append(decision)
        #             break
        # return decisions
