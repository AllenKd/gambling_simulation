import mongoengine
from strategy_provider.common.decision import Decision


class Bet(mongoengine.Document):
    banker_side = mongoengine.StringField("^[(local)|(national)]$")
    type = mongoengine.StringField("^[(total_point)|(spread_point)|(original)]$")
    result = mongoengine.StringField("^[(under)|(over)|(guest)|(host)]$")
    unit = mongoengine.IntField(min_value=0)


class Put(mongoengine.Document):
    name = mongoengine.StringField()
    parameters = mongoengine.DictField()


class Strategy(mongoengine.Document):
    bet = mongoengine.ReferenceField(Bet)
    put = mongoengine.ReferenceField(Put)


class BattleHistory(mongoengine.Document):
    play_time = mongoengine.DateTimeField()
    game_type = mongoengine.StringField("^[(NBA)|(MLB)|(NPB)]$")
    game_time = mongoengine.DateTimeField()
    gamble_id = mongoengine.StringField()
    bet = mongoengine.ReferenceField(Bet)
    confidence = mongoengine.FloatField()
    match = mongoengine.BooleanField()
    capital_before = mongoengine.IntField()
    capital_after = mongoengine.IntField()


class Gambler(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    capital = mongoengine.IntField()
    strategy = mongoengine.ReferenceField(Strategy, db_field="strategy")
    battle_history = mongoengine.ListField(mongoengine.ReferenceField(BattleHistory))

    meta = {
        "indexes": [
            "strategy.bet.name",
            "strategy.put.name",
            {"fields": "name", "unique": True},
        ],
    }

    def __str__(self):
        return f"gambler_name: {self.name}, bet strategy: {self.strategy.bet.name}, put strategy: {self.strategy.put.name}"
