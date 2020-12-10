from binance.client import Client
import time
import json
from decouple import config
import requests

MAINTENANCE_SLEEP_TIME = 30

TRADING_PAIR = "BTCUSDT"

API_SECRET = config("API_SECRET")
API_KEY = config("API_KEY")

ASSETS = ["USDT", "BTC"]


def check_asset_balances(client):
    log_str = "[ASSETS]"
    for asset in ASSETS:
        balance = client.get_asset_balance(asset=asset)
        log_str += f" {asset}(free|locked): ({balance['free']}|{balance['locked']})"
    print(log_str)


def main():
    print("[STATUS] Initializing Binance client..")
    client = Client(API_KEY, API_SECRET)
    check_asset_balances(client)
    STATUS_OK = False
    while True:
        try:
            status = client.get_system_status()
            if status["status"] == 0:  # normal
                print("[STATUS] Normal.") if not STATUS_OK else False
                STATUS_OK = True
                BTCUSDT_PRICE = client.get_ticker(symbol="BTCUSDT")
                print(
                    f"[BTCUSDT] current: {BTCUSDT_PRICE['lastPrice']} change: {BTCUSDT_PRICE['priceChange']}"
                )
                time.sleep(10)

            elif status["status"] == 1:  # system maintenance
                print("[STATUS] !!!System maintenance!!!") if STATUS_OK else False
                STATUS_OK = False
                time.sleep(MAINTENANCE_SLEEP_TIME)

        except requests.exceptions.ReadTimeout:
            print("[STATUS] requests.exceptions.ReadTimeoutError")


if __name__ == "__main__":
    # from helper import get_all_binance
    while True:
        try:
            main()
        except:
            print("[STATUS|WARNING] Something went wrong... Restarting client.")
    #
    # #
    # # timestamp,
    # # open,
    # # high,
    # # low,
    # # close,
    # # volume,
    # # close_time,
    # # quote_av,
    # # trades,
    # # tb_base_av,
    # # tb_quote_av,
    # # ignore
    # import pandas as pd
    # import pandas_ta as ta
    #
    # df = get_all_binance(TRADING_PAIR, "5m", save=True)
    #
    # # Calculate Returns and append to the df DataFrame
    # df.ta.log_return(cumulative=True, append=True)
    # df.ta.percent_return(cumulative=True, append=True)
    #
    # # New Columns with results
    # df.columns
    #
    # # Take a peek
    # print(df.tail())
    # df.tail()

    # print(df)
    # main()
