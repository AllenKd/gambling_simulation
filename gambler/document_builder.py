from strategy_provider.common.decision import Decision
from db.collection.gambler import BattleHistory, Bet


def parse_decision(decision: Decision) -> BattleHistory:
    return BattleHistory(
        game_type=decision.game_type,
        game_time=decision.game_time,
        gamble_id=decision.gamble_id,
        match=decision.match,
        confidence=decision.confidence,
        bet=Bet(
            banker_side=decision.bet.banker_side,
            type=decision.bet.type,
            result=decision.bet.result,
            unit=decision.bet.unit,
        )
    )
