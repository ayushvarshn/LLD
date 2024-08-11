"""
Stock Exchange

Trader can send Buy & sell Request
Example of an order - Buy 10@90 -> Buy quantity 10 at $90

First come first serve - if servable
Trade is allowed if buyPrice >= sellPrice

Match and execute the trade 
"""

from collections import deque
from enum import Enum
import logging
logging.basicConfig(level=logging.INFO)

class OrderType(Enum):
    SELL    = "SELL"
    BUY     = "BUY"

class OrderBook:
    
    def __init__(self) -> None:
        self.start : Order   = None
        self.last : Order    = None
    
    def addOrder(self, order):
        if not self.last:
            self.last = order
            self.start = order
            return
        self.last.next = order
        self.last = order

    def executeTrade(self, orderA, orderB):
        buyOrder    = orderA if orderA.orderType == OrderType.BUY else orderB
        sellOrder   = orderB if orderB.orderType == OrderType.SELL else orderA

        if sellOrder.quantity >= buyOrder.quantity:
            sellOrder.quantity = sellOrder.quantity - buyOrder.quantity
            buyOrder.quantity = 0

        elif sellOrder.quantity < buyOrder.quantity:
            buyOrder.quantity = buyOrder.quantity - sellOrder.quantity
            sellOrder.quantity = 0 
            
            
 
    def matchOrder(self, order):
        prev = None
        start = self.start
        while start is not None:
            
            if self.isMatching(order, start):
                logging.info(f"Trade Matched : {order} -> {start}")
                self.executeTrade(start, order)

                if start.quantity == 0:
                    if not prev:
                        self.start = start.next
                    else:
                        prev.next = start.next

                if order.quantity == 0:
                    return True

            prev = start
            start = start.next
        return False

    def isMatching(self, orderA, orderB):
        if orderA.orderType == OrderType.BUY and orderB.orderType == OrderType.SELL:
            return orderA.price >= orderB.price
        if orderA.orderType == OrderType.SELL and orderB.orderType == OrderType.BUY:
            return orderA.price <= orderB.price
        print("Invalid Order Type to Match for  : %s and %s", orderA, orderB)

    def __str__(self) -> str:
        start = self.start
        output = ""
        while start:
            output += str(start) + " "
            start = start.next
        return output
    
class Order:
    
    def __init__(self, price, quantity, orderType) -> None:
        self.price      = price
        self.orderType  = orderType
        self.quantity   = quantity
        self.next       = None
        

    def __str__(self) -> str:
        return f"[{self.orderType.name} {self.quantity}@{self.price}]"
    
class StockExchange:

    _instance = None

    def __init__(self) -> None:
        self._buyBook = OrderBook()
        self._sellBook = OrderBook()

    def __new__(cls):
        if cls._instance:
            return cls._instance
        cls._instance  = super().__new__(cls)
        return cls._instance

    def displayOrderBook(self):
        print("Buy Book :",self._buyBook)
        print("Sell Book : ",self._sellBook)
        
    def buy(self, price, quantity):
        buyOrder = Order(price, quantity, OrderType.BUY)    
        logging.info(f"Order received : {buyOrder}")   
        if not self._sellBook.matchOrder(buyOrder):
            self._buyBook.addOrder(buyOrder)
        self.displayOrderBook()

    def sell(self, price, quantity):
        sellOrder = Order(price, quantity, OrderType.SELL)   
        logging.info(f"Order received :{sellOrder} ")     
        if not self._buyBook.matchOrder(sellOrder):
                self._sellBook.addOrder(sellOrder)
        self.displayOrderBook()
    
se = StockExchange()
se.buy(80,10)
se.buy(100,4)
se.buy(95, 25)

se.sell(90,5)
se.sell(92,15)
