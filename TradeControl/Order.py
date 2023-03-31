import uuid
import random
from datetime import datetime
from typing import List
from ClientSocketControl import DataStructure
from TradeControl.OrderActionConstants import Action, Direction, ExpiryDate, StrikePrice
from TradeControl.Profile import Profile
import json


class Order:
    def __init__(self, symbol, action, direction, sp, ed, quantity, remained, lastUpdateDateTime):
        self.symbol = symbol
        self.orderid = uuid.uuid4().hex
        self.orderDateTime = datetime.now()
        self.action = action
        self.direction = direction
        self.sp = sp
        self.ed = ed
        self.quantity = quantity
        if remained is None:
            self.remained = quantity
        else:
            self.remained = remained
        if lastUpdateDateTime is None:
            self.lastUpdateDateTime = self.orderDateTime
        else:
            self.lastUpdateDateTime = lastUpdateDateTime
        self.history = [Order(self.symbol, self.action, self.direction, self.sp, self.ed, self.quantity, self.remained, self.lastUpdateDateTime)]

    def trade(self, profile: Profile, data: DataStructure, slippage: float) -> json:
        if self.direction is None and self.sp is None and self.ed is None:
            if self.remained > 0:
                temp_trade_amount = min(data.get_volumn(), self.remained)
                self.traded += temp_trade_amount
                self.remained -= temp_trade_amount
                temp_trade_price = data.get_index() + ((data.get_index() * slippage) * (1 if self.random.randint(0, 1) == 0 else -1))
                self.averageTradePrice = (self.averageTradePrice + (temp_trade_amount * temp_trade_price)) / self.traded
                temp_maket = Order(self.symbol, self.action, self.direction, self.sp, self.ed, self.quantity, self.remained, self.lastUpdateDateTime)
                self.history.append(temp_maket)
                # Update profile
                if self.action == Action.SELL:
                    temp_trade_amount *= -1
                profile.update(self.symbol, temp_trade_amount, temp_trade_price)
                return json.dumps(self.__dict__)
        return None