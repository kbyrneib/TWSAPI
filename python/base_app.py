from ibapi.client import *
from ibapi.wrapper import *

import threading, inspect, time

class BaseApp(EClient, EWrapper):
    def __init__(self, host="localhost", port=7497, client_id=0):
        self.host = host
        self.port = port
        self.client_id = client_id

        EClient.__init__(self, wrapper=self)
        
        self.connect(host, port, client_id)
        
        thread = threading.Thread(target=self.run)
        thread.start()

        # Wait for connection to establish
        start = time.time()
        while not self.isConnected():
            if time.time() - start > 5:
                print("Connection timeout!")
                self.disconnect()
                exit(1)

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
    
    def error(self, reqId, errorTime, errorCode, errorString, advancedOrderRejectJson=""): pass

    def connectionClosed(self):
        self.connect(self.host, self.port, self.client_id)

    # Dynamically read all responses, without having to implement the EWrapper functions directly
    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        
        # Check if returned attribute is a function, is a member of EWrapper and is not one of the proto function
        if callable(attr) and hasattr(EWrapper, name) and name.lower() and "proto" not in name.lower():
                def get_response(*response):
                    # Retrieve list of function parameters and map to returned values
                    params = list(inspect.signature(attr).parameters.keys())
                    mapped_responses = dict(zip(params, response))

                    # Print resulting function name and mapped responses
                    print(f"{name.upper()}: {mapped_responses}")

                    return attr(*response)
                
                return get_response
        
        return attr