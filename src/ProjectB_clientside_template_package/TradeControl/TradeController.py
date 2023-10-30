from typing import List, Union
from ProjectB_clientside_template_package.ClientSocketControl import DataStructure
from ProjectB_clientside_template_package.TradeControl.Order import Order
from ProjectB_clientside_template_package.TradeControl.OrderActionConstants import Action, Direction, ExpiryDate, StrikePrice
from ProjectB_clientside_template_package.TradeControl.Profile import Profile
import json
import random


class TradeController:
    def __init__(self):
        self.profile = Profile()
        self.orders: List[Order] = []
        self.trade_notification_list = []
        self.trade_notification = None
        self.slippage = 0.0
        self.random = random.Random()
    
    def tradeCheckingAndBalanceUpdate(self, ds: DataStructure):
        self.trade_notification_list = []
        for order in self.orders:
            self.trade_notification = order.trade(self.profile, ds, self.slippage)
            if self.trade_notification is not None:
                self.trade_notification_list.append(self.trade_notification)
        
        # update profile balance
        self.profile.balance = 0.0
        for symbol, quantity in self.profile.holding.items():
            if symbol == ds.symbol:
                self.profile.balance += quantity * ds.index
        self.profile.balance += self.profile.cash
        
        # return
        if self.trade_notification_list:
            return json.dumps(self.trade_notification_list)
        else:
            return None
    
    def setSlippage(self, percentage: float):
        self.slippage = percentage
    
    def placeOrder(self, symbol: str, action: str, quantity: int, direction=None, sp=None, ed=None):
        self.orders.append(Order(symbol, action, direction, sp, ed, quantity, None, None, None, None, False))

    def placeOrder(self, symbol: str, action: str, direction=None, sp=None, ed=None):
        if len(self.profile.holding) > 0:
            self.tempOffQuantity = self.profile.holding[symbol]*-1
            if self.tempOffQuantity != 0:
                self.orders.append(Order(symbol, action, direction, sp, ed, self.tempOffQuantity, None, None, None, None, False))
    
    def getProfile(self):
        profile_dict = self.profile.__dict__
        if profile_dict:
            return json.loads(json.dumps(profile_dict))
        else:
            return None
