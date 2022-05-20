import csv
import random
import alpaca_trade_api as tradeapi
import time
import yaml
from pushbullet import Pushbullet

#imports the api keys
CONFIG_FILE = 'auth.yaml'
with open(CONFIG_FILE, 'r') as config_file:
    config = yaml.safe_load(config_file)
    API_KEY_ID = config['alpaca']['API_KEY_ID']
    SECRET_KEY = config['alpaca']['SECRET_KEY']
    APCA_API_BASE_URL = config['alpaca']['APCA_API_BASE_URL']
    Pushbullet_API_KEY = config['pushbullet']['API_KEY']

#setup of the Pushbullet Api
pb = Pushbullet(Pushbullet_API_KEY)

#reads the csv and puts the values on a list
with open('constituents_csv.csv', 'r') as file:
    reader = csv.reader(file)
    rows = []
    for row in reader:
        rows.append(row)

#random number for the stock
numero_random = random.randrange(1,len(rows))
symbol = rows[numero_random][0]

#setup for the alpaca API
api = tradeapi.REST(API_KEY_ID, SECRET_KEY, APCA_API_BASE_URL)

clock = api.get_clock()


def profit(money):
    #insert here your starting money
    starting_money = 200000
    if money > starting_money:
        profit = (money/starting_money * 100) - 100
        profit = round(profit, 2)
        return "🟢Profited +" + str(profit) + "%🟢"
    elif money < starting_money:
        profit = (starting_money /money * 100)-100
        profit = round(profit, 2)
        return"🔴Lost -" + str(profit) + "%🔴"
    else:
        return"Stayed at the same"

#function that buys the stock
def buy(symbol):
    api.close_all_positions()
    time.sleep(2)
    account = api.get_account()
    money = int(float(account.buying_power))
    profit_message = profit(money)
    if money != 0:
        api.submit_order(
            symbol = symbol,
            notional = money,
            side='buy',
            type='market',
            time_in_force= "day")
        print("Bought " + str(money) + " USD of " + rows[numero_random][1] + " (" + symbol +").\n" + profit_message)
        push = pb.push_note("RandomTradeBot", "Bought " + str(money) + " USD of " + 
                            rows[numero_random][1] + " (" + symbol +").\n" + profit_message)
    else:
        print("Error: money = 0")



buy(symbol)

#while True:
#    if clock.is_open :
#        buy(symbol)
#    
#    time.sleep(86400)

