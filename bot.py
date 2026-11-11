import os
import time
import logging
from dotenv import load_dotenv
from binance import Client
from binance.exceptions import BinanceAPIException

# 1. Load secret keys from .env
load_dotenv()

# 2. Set up logging to bot.log and the screen
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
        
        # Sync our bot's clock with Binance's server clock to avoid Timestamp errors!
        server_time = self.client.futures_time()["serverTime"]
        local_time = int(time.time() * 1000)
        self.client.timestamp_offset = server_time - local_time
        
        logging.info("BasicBot initialized, clock synced, and connected to Binance Futures Testnet.")

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        """Sends a Buy or Sell order to Binance Futures Testnet."""
        try:
            # Prepare the basic order details and give a generous 10-second window (recvWindow)
            params = {
                "symbol": symbol.upper(),
                "side": side.upper(),
                "type": order_type.upper(),
                "quantity": quantity,
                "recvWindow": 10000
            }

            # Limit orders need a specific price and 'timeInForce' (GTC = Good Till Cancelled)
            if order_type.upper() == "LIMIT":
                params["price"] = price
                params["timeInForce"] = "GTC"

            # Bonus: Stop-Limit orders need both a trigger (stopPrice) and a limit price
            elif order_type.upper() == "STOP":
                params["price"] = price
                params["stopPrice"] = stop_price
                params["timeInForce"] = "GTC"

            # Write down what we are sending in our diary (bot.log)
            logging.info(f"Sending API Request: {params}")

            # Actually send the order to Binance Futures!
            response = self.client.futures_create_order(**params)

            # Write down the response from Binance in our diary
            logging.info(f"API Response received: {response}")
            return response

        except BinanceAPIException as e:
            logging.error(f"Binance API Error: {e.status_code} - {e.message}")
            return None
        except Exception as e:
            logging.error(f"Unexpected Error: {str(e)}")
            return None

#test to place a practice Market Buy order for Bitcoin (BTCUSDT)!
if __name__ == "__main__":
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    bot = BasicBot(api_key, api_secret, testnet=True)
    
    print("Placing a test Market BUY order for 0.01 Bitcoin (BTCUSDT)...")
    result = bot.place_order(symbol="BTCUSDT", side="BUY", order_type="MARKET", quantity=0.01)
    
    if result:
        print("\nOrder Placed Successfully!")
        print(f"Order ID: {result.get('orderId')}")
        print(f"Status: {result.get('status')}")