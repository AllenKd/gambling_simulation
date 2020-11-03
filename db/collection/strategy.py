import mongoengine


class Strategy(mongoengine.Document):
    name = mongoengine.StringField()
    parameters = mongoengine.DictField()
    put_strategy = mongoengine.StringField()


class BattleData:
    gambler_id = mongoengine.StringField()
    strategy = mongoengine.ReferenceField(Strategy)
    # decision =
