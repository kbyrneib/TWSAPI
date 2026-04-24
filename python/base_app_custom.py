from ibapi.client import *
from ibapi.wrapper import *

import threading, time

"""
Create child class that inherits from BaseAppCustom
Then, just add any extra callbacks you neeed
Or, just add the callbacks directly to BaseAppCustom
"""

class BaseAppCustom(EClient, EWrapper):
    def __init__(self, host="localhost", port=7497, client_id=0):
        self.host = host
        self.port = port
        self.client_id = client_id

        EClient.__init__(self, wrapper=self)
        
        self.connect(host, port, client_id)
        
        thread = threading.Thread(target=self.run)
        thread.start()

        # Wait for nextValidId callback
        start = time.time()
        while not hasattr(self, "order_id"):
            if time.time() - start > 5:
                print("Timeout waiting for nextValidId!")
                self.disconnect()
                exit(1)

    def nextValidId(self, orderId):
        self.order_id = orderId

    def nextId(self):
        self.order_id += 1
        return self.order_id
    
    def error(self, reqId, errorTime, errorCode, errorString, advancedOrderRejectJson=""):
        print(reqId, errorTime, errorCode, errorString, advancedOrderRejectJson)

    def connectionClosed(self):
        self.connect(self.host, self.port, self.client_id)