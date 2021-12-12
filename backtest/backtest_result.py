import json


class BacktestResult:
    def __init__(self, performance):
        self.performance = performance

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)