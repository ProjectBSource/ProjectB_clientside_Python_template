from enum import Enum


class Action(Enum):
    BUY = "BUY"
    SELL = "SELL"
    OFF = "OFF"
    
    def getAction(self):
        return self.value
