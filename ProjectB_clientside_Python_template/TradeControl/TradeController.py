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
        self.orders = {}
        self.trade_notification_list = []
        self.trade_notification = None
        self.slippage = 0.0
        self.random = random.Random()
    
    def tradeCheckingAndBalanceUpdate(self, ds: DataStructure):
        self.trade_notification_list = []
        self.trade_notification = None

        for order in self.orders:
            self.trade_notification = order.trade(self.profile, ds, self.slippage)
            if self.trade_notification is not None:
                self.trade_notification_list.append(self.trade_notification)
        
        # Move the completed OFF trade to completedOrders arraylist
        tempNewOrders = self.orders.copy()
        for order in self.orders.items():
            if "_OFF" in order[0]:
                if order[1].remained == 0:
                    self.completedOrders.append(order[1])
                    tempNewOrders.pop(order[0])
        self.orders = tempNewOrders

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
    
    def placeOrder(self, id: str, symbol: str, action: str, quantity: int, direction, sp, ed, oneTimeTradeCheck):
        if id not in self.orders:
            self.orders[id] = Order(id, symbol, action, direction, sp, ed, quantity, None, None, None, None, False, oneTimeTradeCheck)
            return True
        return False

    def placeOFFOrder(self, targetId: str, dataStructure: DataStructure):
        order = self.orders.get(targetId)
        if order:
            if self.profile.holding:
                if order.symbol in self.profile.holding:
                    if self.profile.holding[order.symbol] >= order.traded:
                        # For All trade off
                        if order.action == Action.BUY:
                            self.orders[targetId + "_OFF"] = Order(targetId+"_OFF", order.symbol, Action.SELL, order.direction, order.sp, order.ed, order.traded, None, None, None, None, False, order.oneTimeTradeCheck)
                        elif order.action == Action.SELL:
                            self.orders[targetId + "_OFF"] = Order(targetId+"_OFF", order.symbol, Action.BUY,  order.direction, order.sp, order.ed, order.traded, None, None, None, None, False, order.oneTimeTradeCheck)
                        if order.oneTimeTradeCheck==False:
                            self.completedOrders.append(order)
                            self.orders.pop(targetId)
                        return True
        return False

    def getProfile(self):
        profile_dict = self.profile.__dict__
        if profile_dict:
            return json.loads(json.dumps(profile_dict))
        else:
            return None
