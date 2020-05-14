class GambleRecord:
    def __init__(self, gambler_id, strategy):
        self.content = {
            "gambler_id": gambler_id,
            "strategy": {
                "name": strategy.name,
                "parameters": strategy.parameters,
                "put_strategy": strategy.put_strategy.name,
            },
        }

    def __str__(self):
        return self.content
