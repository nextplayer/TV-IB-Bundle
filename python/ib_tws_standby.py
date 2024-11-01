from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.client import Contract, Order
from threading import Thread
import time, datetime
from flask import Flask, request, jsonify

# default host
DEFAULT_HOST = '127.0.0.1'
DEFAULT_CLIENT_ID = 1
# trading mode
PAPER_TRADING = True
TRADING_PORT = 7497 if PAPER_TRADING else 7496
FLASK_PORT = 5001
# supported types
SUPPORTED_FUTURES = {'MES':'CME', 'MNQ':'CME'}
SUPPORTED_ACTIONS = ['BUY', 'SELL']
SUPPORTED_ORDER_TYPES = ['MKT', 'LMT']

app = Flask(__name__)

class IBClient(EWrapper, EClient):
    def __init__(self, host, port, client_id):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.connected = False
        self.connect(host, port, client_id)
        thread = Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def error(self, req_id, code, msg, misc):
        print(f'Error {code}: {msg}' if code not in [2104, 2106, 2158] else msg)

    def nextValidId(self, orderId: int):
        self.order_id = orderId
        print(f"next valid id is {self.order_id}")

    # callback to log order status, we can put more behavior here if needed
    def orderStatus(self, order_id, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print(f"order status {order_id} {status} {filled} {remaining} {avgFillPrice}")    


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return jsonify({
            "status": "ok",
            "message": "Server is running",
            "endpoints": {
                "place_order": "/place_order (POST)"
            }
        })
    else:  # POST
        return jsonify({
            "status": "error",
            "message": "Please use /place_order endpoint for placing orders",
            "correct_endpoint": "/place_order"
        }), 400

def check_connection():
    if not client or not hasattr(client, 'order_id'):
        return jsonify({"status": "error", "message": "Not connected to IB"}), 503
@app.route('/place_order', methods=['POST'])
def place_order():
    try:
        conn_check = check_connection()
        if conn_check:
            return conn_check
        data = request.json
        # validate required fields
        required_fields = ['action', 'symbol', 'quantity', 'type']
        for field in required_fields:
            if field not in data:
                return jsonify({"status": "error", "message": f"Missing {field}"}), 400
        
        action = data['action'].upper()
        symbol = data['symbol'].upper()
        quantity = data['quantity']
        order_type = data['type'].upper()
        price = data.get('price')
        
        # validate action 
        if action not in SUPPORTED_ACTIONS:
            return jsonify({"status": "error", "message": "Invalid action"}), 400
        # validate type 
        if order_type not in SUPPORTED_ORDER_TYPES:
            return jsonify({"status": "error", "message": "Invalid type"}), 400
        # validate price for LMT orders
        if order_type == 'LMT' and not price:
            return jsonify({"status": "error", "message": "Price is required for limit orders"}), 400

        # place order 
        execute_order(action, symbol, quantity, order_type, price)
        
        if order_type == "LMT":  # limit order
            message = f"{order_type} {action} order placed for {quantity} {symbol} at {price}"
        else:  # market order
            message = f"{order_type} {action} order placed for {quantity} {symbol}"

        return jsonify({"status": "success", "message": message})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def execute_order(action, symbol, quantity, order_type, price):
    contract = Contract()
    contract.symbol = symbol
    contract.currency = "USD"
    if symbol in SUPPORTED_FUTURES:  # futures code
        contract.secType = 'FUT'
        contract.exchange = SUPPORTED_FUTURES[symbol]
        contract.lastTradeDateOrContractMonth = get_next_contract_month()
    else:
        contract.secType = "STK"
        contract.exchange = "SMART"

    order = Order()
    order.orderType = order_type
    order.lmtPrice = price;
    order.totalQuantity = quantity
    order.action = action
    
    client.reqIds(-1)  # request new order ID
    time.sleep(2)  # wait to get order ID
    
    if not client.order_id:
        raise Exception("Failed to get order ID")
    
    print(f"Got order id, placing {action} order")
    client.placeOrder(client.order_id, contract, order)

def get_next_contract_month():
    # this function returns next contract month
    # here is a simple implementation, you may need to adjust according to actual situation
    now = datetime.datetime.now()
    month = now.month
    year = now.year
    if month >= 12:
        month = 3
        year += 1
    elif month >= 9:
        month = 12
    elif month >= 6:
        month = 9
    elif month >= 3:
        month = 6
    else:
        month = 3
    return f"{year}{month:02d}"

if __name__ == '__main__':
    try:
        client = IBClient(DEFAULT_HOST, TRADING_PORT, DEFAULT_CLIENT_ID)
        time.sleep(1)
        
        if not hasattr(client, 'order_id'):
            print("Failed to connect to IB")
            exit(1)
            
        print("Connected to IB successfully")
        print(f"Starting Flask server on port {FLASK_PORT}")
        app.run(port=FLASK_PORT)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)
# ngrok http http://127.0.0.1:5001
