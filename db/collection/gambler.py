import mongoengine


class Bet(mongoengine.Document):
    name = mongoengine.StringField()
    parameters = mongoengine.DictField()


class Put(mongoengine.Document):
    name = mongoengine.StringField()
    parameters = mongoengine.DictField()


class Strategy(mongoengine.Document):
    bet = mongoengine.ReferenceField(Bet)
    put = mongoengine.ReferenceField(Put)


class Gambler(mongoengine.Document):
    name = mongoengine.StringField()
    capital = mongoengine.IntField()
    strategy = mongoengine.ReferenceField(Strategy, db_field="strategy")

    meta = {
        "indexes": ["strategy.bet.name", "strategy.put.name"],
    }

    def __str__(self):
        return f"gambler_name: {self.name}, bet strategy: {self.strategy.bet.name}, put strategy: {self.strategy.put.name}"
