from banker.banker import Banker


class Decision:
    def __init__(self, game_type, game_date, gamble_id, bet, **kwargs):
        self.game_type = game_type
        self.game_date = game_date
        self.gamble_id = gamble_id

        self.bet = bet
        self.match = None
        self.confidence = kwargs.get("confidence", None)

    def __str__(self):
        return "type: %s, date: %s, id: %s, bet: %s, confidence: %s" % (
            self.game_type,
            self.game_date,
            self.gamble_id,
            self.bet,
            self.confidence,
        )

    def get_response(self):
        gamble_info = Banker().get_gamble_info(
            self.game_date, game_type=self.game_type, gamble_id=self.gamble_id,
        )
        if len(gamble_info) != 1:
            raise Exception(f"unexpected gamble info result: {gamble_info}")

        return gamble_info[0].gamble_info[self.bet.type]["response"][self.bet.result]


class Bet:
    def __init__(self, banker_side, bet_type, result, unit=1):
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


class Confidence:
    side = None
    index = 0

    def __str__(self):
        return f"side: {self.side}, index: {self.index}"


def get_confidence(side_vote) -> Confidence:
    side_1 = list(side_vote)[0]
    side_2 = list(side_vote)[1]

    # invalid gamble if votes are 0
    assert side_vote[side_1]["population"] or side_vote[side_2]["population"]

    c = Confidence
    c.side = (
        side_1
        if side_vote[side_1]["population"] > side_vote[side_2]["population"]
        else side_2
    )

    major = max(side_vote[side_1]["population"], side_vote[side_2]["population"])
    minor = min(side_vote[side_1]["population"], side_vote[side_2]["population"]) or 0.1
    c.index = major / minor * (major - minor)
    return c
