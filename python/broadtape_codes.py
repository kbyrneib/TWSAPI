from ibapi.client import *
from ibapi.wrapper import *

import threading, time, csv

"""
Running this script directly will produce the file news_codes.csv

The headers of this CSV file are Symbol, Name, Subject

The Subject is stored in the tradingClass of the Contract object

The Symbol may be used to build a Contract for a subsequent Broadtape news request e.g.:

contract = Contract()
contract.symbol  = "BRFUPDN:BRF_ALL"
contract.secType = "NEWS"
contract.exchange = "BRFUPDN"

self.reqMktData(reqId, contract, "mdoff,292", False, False, [])
"""

class NewsApp(EClient, EWrapper):
    def __init__(self, host="localhost", port=7497, client_id=0):
        self.host = host
        self.port = port
        self.client_id = client_id

        EClient.__init__(self, wrapper=self)
        
        self.connect(host, port, client_id)
        
        thread = threading.Thread(target=self.run)
        thread.start()

        start = time.time()
        while not hasattr(self, "order_id"):
            if time.time() - start > 5:
                print("Timeout waiting for nextValidId!")
                self.disconnect()
                exit(1)

        self.providers = ["BRFG", "BRFUPDN", "BZ", "DJ", "DJNL", "DJTOP", "FLY"]
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
        if self.num_requests == len(self.providers):
            with open('news_codes.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Symbol", "Name", "Subject"])
                writer.writerows(self.news_codes)
            
            print("Provider codes saved to news_codes.csv")

app = NewsApp()

for provider in app.providers:
    contract = Contract()
    contract.secType = "NEWS"
    contract.exchange = provider

    app.reqContractDetails(app.nextId(), contract)