import mongoengine
from gambler.gambler import Gambler


# class GambleRecord:
#     def __init__(self, gambler_id, strategy):
#         self.content = {
#             "gambler_id": gambler_id,
#             "strategy": {
#                 "name": strategy.name,
#                 "parameters": strategy.parameters,
#                 "put_strategy": strategy.put_strategy.name,
#             },
#         }
#
#     def __str__(self):
#         return self.content

class Get(mongoengine.Document):
    banker_side = mongoengine.StringField()
    type = mongoengine.StringField()
    result = mongoengine.StringField()
    unit = mongoengine.IntField(min_value=0)


class GambleHistory(mongoengine.Document):
    game_type = mongoengine.StringField()
    game_time = mongoengine.DateTimeField()
    gamble_id = mongoengine.StringField()
    bet = mongoengine.ReferenceField(Get)
    win = mongoengine.BooleanField()


class BattleRecord(mongoengine.Document):
    gambler_name = mongoengine.StringField()
    gamble_history = mongoengine.ReferenceField(GambleHistory)

    def from_latest_decision(self, gambler: Gambler):
        latest_decision = gambler.decision_history[-1]
        br = BattleRecord(
            gambler_name=gambler.name,
            gamble_history=GambleHistory(
                game_type=latest_decision.game_type,
                game_time=latest_decision.
            )
        )

