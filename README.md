# Crypto Trading Bot - Binance Futures Testnet

A Python-based trading bot for the Binance Futures Testnet (USDT-M) supporting Market, Limit, and Stop-Limit orders via an interactive CLI.

## Features
- **Order Types:** Market, Limit, and Stop-Limit (Bonus) orders on both `BUY` and `SELL` sides.
- **Interactive CLI:** Validates user inputs (symbols, sides, positive quantities, and prices).
- **Logging & Error Handling:** Records all API requests, responses, and errors to `bot.log`.
- **Automatic Clock Sync:** Synchronizes with Binance server time to prevent timestamp (`recvWindow`) errors.

## Setup Instructions
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt