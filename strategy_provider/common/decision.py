class Decision:
    def __init__(self, game_type, game_date, gamble_id, bet, **kwargs):
        self.game_type = game_type
        self.game_date = game_date
        self.gamble_id = gamble_id

        # list fo Bet object
        self.bet = bet
        self.match = None
        self.confidence = kwargs.get('confidence', None)

    def __str__(self):
        return "type: %s, date: %s, id: %s, bet: %s" % (
            self.game_type,
            self.game_date,
            self.gamble_id,
            self.bet,
        )


class Bet:
    def __init__(self, banker_side, bet_type, result, unit):
        self.banker_side = banker_side
        self.type = bet_type
        self.result = result
        self.unit = unit

    def __str__(self):
        return "banker_side: %s, result: %s, unit: %s" % (
            self.banker_side,
            self.result,
            self.unit,
        )
