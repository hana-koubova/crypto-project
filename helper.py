from flask import request
import requests
import json


def get_crypto_list():
    url = "https://api.coingecko.com/api/v3/coins/list"
    headers = {"accept": "application/json"}
    all_coins_response = requests.get(url, headers=headers)
    all_coins = json.loads(all_coins_response.text)
    #coin_names = []
    #for coin in all_coins:
    #    coin_names.append(coin['name'])
    return all_coins

def check_for_symbol(symbol):
    url = "https://api.coingecko.com/api/v3/coins/list"
    headers = {"accept": "application/json"}
    all_coins_response = requests.get(url, headers=headers)
    all_coins = json.loads(all_coins_response.text)
    #all_coins = get_crypto_list()
    for coin in all_coins:
        if coin['symbol'] == symbol:
            print(coin)
            return coin
            
    return False
