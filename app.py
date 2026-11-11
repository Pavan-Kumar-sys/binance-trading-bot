import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from bot import BasicBot

# Load secret keys from .env
load_dotenv()

app = Flask(__name__)

# Initialize our bot using the keys from .env
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
bot = BasicBot(api_key, api_secret, testnet=True) if (api_key and api_secret) else None

@app.route("/")
def index():
    """Shows the main interactive web page."""
    return render_template("index.html")

@app.route("/api/order", methods=["POST"])
def place_order():
    """Receives order details from the web page and sends them to Binance."""
    if not bot:
        return jsonify({"success": False, "error": "API keys are missing in .env file!"}), 400

    data = request.json
    symbol = data.get("symbol", "BTCUSDT").strip().upper()
    side = data.get("side", "BUY").strip().upper()
    order_type = data.get("order_type", "MARKET").strip().upper()

    # Validate quantity
    try:
        quantity = float(data.get("quantity", 0))
        if quantity <= 0:
            return jsonify({"success": False, "error": "Quantity must be greater than 0."}), 400
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Invalid quantity number."}), 400

    price = None
    stop_price = None

    # Validate Limit Price if needed
    if order_type in ["LIMIT", "STOP"]:
        try:
            price = float(data.get("price", 0))
            if price <= 0:
                return jsonify({"success": False, "error": "Limit price must be greater than 0."}), 400
        except (ValueError, TypeError):
            return jsonify({"success": False, "error": "Invalid limit price."}), 400

    # Validate Stop Price if needed
    if order_type == "STOP":
        try:
            stop_price = float(data.get("stop_price", 0))
            if stop_price <= 0:
                return jsonify({"success": False, "error": "Stop trigger price must be greater than 0."}), 400
        except (ValueError, TypeError):
            return jsonify({"success": False, "error": "Invalid stop trigger price."}), 400

    # Place the order using our BasicBot
    result = bot.place_order(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
        stop_price=stop_price
    )

    if result:
        return jsonify({"success": True, "order": result})
    else:
        return jsonify({"success": False, "error": "Order failed! Check the activity log below for exact Binance API error."}), 400

@app.route("/api/logs", methods=["GET"])
def get_logs():
    """Reads the last 20 lines of bot.log to display on the web page."""
    if os.path.exists("bot.log"):
        with open("bot.log", "r") as f:
            lines = f.readlines()
            return jsonify({"logs": "".join(lines[-20:])})
    return jsonify({"logs": "No logs recorded yet."})

if __name__ == "__main__":
    print("Starting Web Dashboard! Open http://127.0.0.1:5000 in your browser.")
    app.run(debug=True, port=5000)