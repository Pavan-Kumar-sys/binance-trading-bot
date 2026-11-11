import os
from dotenv import load_dotenv
from bot import BasicBot

# Load secret keys from .env
load_dotenv()

def get_valid_choice(prompt, valid_choices):
    """Keeps asking the user until they type one of the allowed words."""
    while True:
        user_input = input(prompt).strip().upper()
        if user_input in valid_choices:
            return user_input
        print(f"Invalid choice! Please type one of these: {', '.join(valid_choices)}")

def get_positive_number(prompt):
    """Keeps asking the user until they type a valid number greater than 0."""
    while True:
        try:
            value = float(input(prompt).strip())
            if value > 0:
                return value
            print("Number must be greater than 0. Try again.")
        except ValueError:
            print("That is not a valid number! Please enter digits only (e.g., 0.01 or 65000).")

def main():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print("Error: API keys not found! Please check your .env file.")
        return

    print("Connecting to Binance Futures Testnet...")
    bot = BasicBot(api_key, api_secret, testnet=True)

    while True:
        print("\n" + "="*45)
        print("   CRYPTO TRADING BOT - FUTURES TESTNET")
        print("="*45)
        print("1. Place a Market Order (Instant Buy/Sell)")
        print("2. Place a Limit Order (Buy/Sell at your target price)")
        print("3. Place a Stop-Limit Order (Bonus: Trigger + Target price)")
        print("4. Exit")
        print("="*45)

        choice = get_valid_choice("Select an option (1/2/3/4): ", ["1", "2", "3", "4"])

        if choice == "4":
            print("Exiting Trading Bot. Goodbye!")
            break

        # 1. Ask for the trading pair (Symbol)
        symbol = input("Enter trading pair symbol (press Enter for BTCUSDT): ").strip().upper()
        if not symbol:
            symbol = "BTCUSDT"

        # 2. Ask for BUY or SELL
        side = get_valid_choice("Enter order side (BUY / SELL): ", ["BUY", "SELL"])

        # 3. Ask for Quantity
        quantity = get_positive_number(f"Enter quantity of {symbol} to {side} (e.g., 0.01): ")

        # 4. Handle the specific order type
        if choice == "1":
            order_type = "MARKET"
            result = bot.place_order(symbol, side, order_type, quantity)

        elif choice == "2":
            order_type = "LIMIT"
            price = get_positive_number("Enter Limit Price (in USDT): ")
            result = bot.place_order(symbol, side, order_type, quantity, price=price)

        elif choice == "3":
            order_type = "STOP"
            stop_price = get_positive_number("Enter Stop Trigger Price (in USDT): ")
            price = get_positive_number("Enter Limit Execution Price (in USDT): ")
            result = bot.place_order(symbol, side, order_type, quantity, price=price, stop_price=stop_price)

        #clean output summary
        print("\n" + "-"*45)
        if result:
            print("ORDER EXECUTED SUCCESSFULLY!")
            print(f"Symbol:       {result.get('symbol')}")
            print(f"Side:         {result.get('side')}")
            print(f"Order Type:   {result.get('type')}")
            print(f"Order ID:     {result.get('orderId')}")
            print(f"Status:       {result.get('status')}")
            print(f"Quantity:     {result.get('origQty')}")
            if result.get('price') and float(result.get('price')) > 0:
                print(f"Limit Price:  {result.get('price')}")
            if result.get('stopPrice') and float(result.get('stopPrice')) > 0:
                print(f"Stop Price:   {result.get('stopPrice')}")
        else:
            print("ORDER FAILED! Please check 'bot.log' or the error message above for details.")
        print("-"*45)

if __name__ == "__main__":
    main()