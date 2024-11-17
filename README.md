# TradingView to IB TWS Order System
Easiest Way to Bundle TradingView and Interactive Brokers Trader Workstation.  
Simplest system to place orders with webhook alerts.

### 1. tv-to-gas.gs
Google Apps Script that receives webhook alerts from TradingView
- Receives POST requests from TradingView
- Validates order data
- Forwards valid orders

### 2. gas-to-ib.gs
Google Apps Script that forwards processed orders to IB TWS
- Sends POST requests to IB TWS server
- Handles order payload formatting
- Logs responses

### 3. ib_tws_standby.py
Python server that connects to IB TWS and executes orders
- Maintains connection with IB TWS
- Provides REST API for order placement
- Supports futures (MES, MNQ) and stocks
- Handles both market and limit orders

## Environment
1. VSCode (`install python3`)
2. python (`python3 -m venv venv`)
3. [ibapi](https://interactivebrokers.github.io/) (`python3 IBJts/source/pythonclient/setup.py install`)
4. flask (`pip install flask`)
5. [ngrok](https://ngrok.com/download)
7. [IB TWS](https://www.interactivebrokers.com/en/trading/tws.php#tws-software)
8. Google Apps Script
9. TradingView

## Setup

1. Deploy `tv-to-gas.gs` and `gas-to-ib.gs` to Google Apps Script  
2. Start IB TWS/Gateway
3. Run `ib_tws_standby.py`
4. Run `ngrok http http://127.0.0.1:5001`
5. Update webhook URLs in TradingView and Google Apps Script

## Supported Orders
- Actions: BUY, SELL
- Types: MKT (Market), LMT (Limit)
- Symbols: MES, MNQ (Futures), Stocks

## Demo
https://youtu.be/kfw_m8GCORk
