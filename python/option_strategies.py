from ibapi.contract import Contract, ComboLeg

def bull_call_vertical_spread(symbol, buy_call, sell_call):
    """
    Bull Call Vertical Spread / Long Call Spread:
    ------------------------
    Buy a call   ->  Strike A (lowest)
    ------------------------
    Underlying price here (at / above Strike A)
    ------------------------
    Sell a call  ->  Strike B (highest)
    ------------------------
    """
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "BAG"
    contract.currency = "USD"
    contract.exchange = "SMART"

    leg1 = ComboLeg()
    leg1.conId = buy_call
    leg1.ratio = 1
    leg1.action = "BUY"
    leg1.exchange = "SMART"

    leg2 = ComboLeg()
    leg2.conId = sell_call
    leg2.ratio = 1
    leg2.action = "SELL"
    leg2.exchange = "SMART"

    contract.comboLegs = []
    contract.comboLegs.append(leg1)
    contract.comboLegs.append(leg2)

    return contract

def bull_put_vertical_spread(symbol, buy_put, sell_put):
    """
    Bull Put Vertical Spread / Short Put Spread:
    ------------------------
    Buy a put   ->  Strike A (lowest)
    Sell a put  ->  Strike B (highest)
    ------------------------
    Underlying price here
    ------------------------
    """
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "BAG"
    contract.currency = "USD"
    contract.exchange = "SMART"

    leg1 = ComboLeg()
    leg1.conId = buy_put
    leg1.ratio = 1
    leg1.action = "BUY"
    leg1.exchange = "SMART"

    leg2 = ComboLeg()
    leg2.conId = sell_put
    leg2.ratio = 1
    leg2.action = "SELL"
    leg2.exchange = "SMART"

    contract.comboLegs = []
    contract.comboLegs.append(leg1)
    contract.comboLegs.append(leg2)

    return contract

def bear_call_vertical_spread(symbol, sell_call, buy_call):
    """
    Bear Call Vertical Spread / Short Call Spread:
    ------------------------
    Underlying price here
    ------------------------
    Sell a call ->  Strike A (lowest)
    Buy a call  ->  Strike B (highest)
    ------------------------
    """
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "BAG"
    contract.currency = "USD"
    contract.exchange = "SMART"

    leg1 = ComboLeg()
    leg1.conId = sell_call
    leg1.ratio = 1
    leg1.action = "SELL"
    leg1.exchange = "SMART"

    leg2 = ComboLeg()
    leg2.conId = buy_call
    leg2.ratio = 1
    leg2.action = "BUY"
    leg2.exchange = "SMART"

    contract.comboLegs = []
    contract.comboLegs.append(leg1)
    contract.comboLegs.append(leg2)

    return contract

def iron_condor(symbol, buy_put, sell_put, sell_call, buy_call):
    """
    Iron Condor (Bull Put Spread + Bear Call Spread):
    ------------------------
    Buy a put   ->  Strike A (lowest)
    Sell a put  ->  Strike B
    ------------------------
    Underlying price here
    ------------------------
    Sell a call ->  Strike C
    Buy a call  ->  Strike D (highest)
    ------------------------
    """
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "BAG"
    contract.currency = "USD"
    contract.exchange = "SMART"

    leg1 = ComboLeg()
    leg1.conId = buy_put
    leg1.ratio = 1
    leg1.action = "BUY"
    leg1.exchange = "SMART"

    leg2 = ComboLeg()
    leg2.conId = sell_put
    leg2.ratio = 1
    leg2.action = "SELL"
    leg2.exchange = "SMART"

    leg3 = ComboLeg()
    leg3.conId = sell_call
    leg3.ratio = 1
    leg3.action = "SELL"
    leg3.exchange = "SMART"

    leg4 = ComboLeg()
    leg4.conId = buy_call
    leg4.ratio = 1
    leg4.action = "BUY"
    leg4.exchange = "SMART"

    contract.comboLegs = []
    contract.comboLegs.append(leg1)
    contract.comboLegs.append(leg2)
    contract.comboLegs.append(leg3)
    contract.comboLegs.append(leg4)

    return contract