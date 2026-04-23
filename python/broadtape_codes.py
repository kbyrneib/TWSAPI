from ibapi.client import *
from ibapi.wrapper import *

import threading, time, csv

class NewsApp(EClient, EWrapper):
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

        self.news_codes = []
        self.num_requests = 0

    def nextValidId(self, orderId):
        self.order_id = orderId

    def nextId(self):
        self.order_id += 1
        return self.order_id

    def contractDetails(self, reqId, contractDetails):
        self.news_codes.append([contractDetails.contract.symbol, contractDetails.longName, contractDetails.contract.tradingClass])

    def contractDetailsEnd(self, reqId):
        self.num_requests += 1
        if self.num_requests == 7:
            with open('news_codes.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Symbol", "Name", "Subject (Trading Class)"])
                writer.writerows(self.news_codes)

app = NewsApp()

providers = ["BRFG", "BRFUPDN", "BZ", "DJ", "DJNL", "DJTOP", "FLY"]

for provider in providers:
    contract = Contract()
    contract.secType = "NEWS"
    contract.exchange = provider

    app.reqContractDetails(app.nextId(), contract)