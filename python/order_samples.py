from ibapi.order import Order

def market_order(action="BUY", quantity=1.0, tif="DAY"):
    order = Order()
    order.orderType = "MKT"
    order.action = action
    order.totalQuantity = quantity
    order.tif = tif

    return order

def limit_order(action="BUY", limit_price=265.0, quantity=1.0, tif="DAY"):
    order = Order()
    order.orderType = "LMT"
    order.action = action
    order.totalQuantity = quantity
    order.tif = tif
    order.lmtPrice = limit_price

    return order

def stop_order(action="BUY", stop_trigger=265.0, quantity=1.0, tif="DAY"):
    order = Order()
    order.orderType = "STP"
    order.action = action
    order.totalQuantity = quantity
    order.tif = tif
    order.auxPrice = stop_trigger

    return order

def stop_limit_order(action="BUY", stop_trigger=265.0, limit_price=266.0, quantity=1.0, tif="DAY"):
    order = Order()
    order.orderType = "STP LMT"
    order.action = action
    order.totalQuantity = quantity
    order.tif = tif
    order.auxPrice = stop_trigger
    order.lmtPrice = limit_price

    return order

def market_if_touched_order(action="BUY", stop_trigger=265.0, quantity=1.0, tif="DAY"):
    order = Order()
    order.orderType = "MIT"
    order.action = action
    order.totalQuantity = quantity
    order.tif = tif
    order.auxPrice = stop_trigger

    return order

def market_to_limit_order(action="BUY", quantity=1.0, tif="DAY"):
    order = Order()
    order.orderType = "MTL"
    order.action = action
    order.totalQuantity = quantity
    order.tif = tif

    return order

def market_on_open_order(action="BUY", quantity=1.0):
    order = Order()
    order.orderType = "MKT"
    order.action = action
    order.totalQuantity = quantity
    order.tif = "OPG"

    return order

def market_on_close_order(action="BUY", quantity=1.0):
    order = Order()
    order.orderType = "MOC"
    order.action = action
    order.totalQuantity = quantity
    order.tif = "DAY"

    return order

def limit_if_touched_order(action="BUY", stop_trigger = 270.0, limit_price=267.0, quantity=1.0, tif="DAY"):
    order = Order()
    order.orderType = "LIT"
    order.action = action
    order.totalQuantity = quantity
    order.tif = tif
    order.auxPrice = stop_trigger
    order.lmtPrice = limit_price

    return order

def limit_on_open_order(action="BUY", limit_price=265.0, quantity=1.0):
    order = Order()
    order.orderType = "LMT"
    order.action = action
    order.totalQuantity = quantity
    order.tif = "OPG"
    order.lmtPrice = limit_price

    return order

def limit_on_close_order(action="BUY", limit_price=265.0, quantity=1.0):
    order = Order()
    order.orderType = "LOC"
    order.action = action
    order.totalQuantity = quantity
    order.tif = "DAY"
    order.lmtPrice = limit_price

    return order

def bracket_order_single(parent):
    parent.ptOrderId = parent.orderId + 1
    parent.ptOrderType = "PRESET"
    parent.slOrderId = parent.orderId + 2
    parent.slOrderType = "PRESET"

    return parent

def bracket_order_multiple(parent, action="BUY", limit_price=265.0, quantity=1.0, tif="DAY"):
    parent.transmit = False

    take_profit = Order()
    take_profit.orderId = parent.orderId + 1
    take_profit.parentId = parent.orderId
    take_profit.orderType = "LMT"
    take_profit.action = "SELL" if action=="BUY" else "BUY"
    take_profit.totalQuantity = quantity
    take_profit.tif = tif
    take_profit.lmtPrice = parent.lmtPrice + 1
    take_profit.transmit = False

    stop_loss = Order()
    stop_loss.orderId = parent.orderId + 2
    stop_loss.parentId = parent.orderId
    stop_loss.orderType = "STP"
    stop_loss.action = take_profit.action
    stop_loss.totalQuantity = quantity
    stop_loss.tif = tif
    stop_loss.auxPrice = parent.lmtPrice - 1
    stop_loss.transmit = True

    return [parent, take_profit, stop_loss]