import csv
import random
from re import L
from turtle import position
import alpaca_trade_api as tradeapi
import time
import yaml
import tweepy
from datetime import date
from pushbullet import Pushbullet

history_file = 'history.txt'

#imports the api keys
CONFIG_FILE = 'auth.yaml'
with open(CONFIG_FILE, 'r') as config_file:
    config = yaml.safe_load(config_file)
    API_KEY_ID = config['alpaca']['API_KEY_ID']
    SECRET_KEY = config['alpaca']['SECRET_KEY']
    APCA_API_BASE_URL = config['alpaca']['APCA_API_BASE_URL']
    Pushbullet_API_KEY = config['pushbullet']['API_KEY']
    twitter_consumer_key = config['twitter']['API Key']
    twitter_consumer_secret = config['twitter']['API Key Secret']
    twitter_access_token = config['twitter']['Access Token']
    twitter_access_token_secret = config['twitter']['Access Token Secret']


auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)

twitter_api = tweepy.API(auth)
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
alpaca_api = tradeapi.REST(API_KEY_ID, SECRET_KEY, APCA_API_BASE_URL)

clock = alpaca_api.get_clock()


def profit(money):
    if money == 0:
        return " "
    #insert here your starting money
    starting_money = 100000
    if money > starting_money:
        profit = ((money/starting_money) * 100) - 100
        profit = round(profit, 2)
        return "+" + str(profit) + "%🟢"
    elif money < starting_money:
        profit = ((starting_money /money) * 100)-100
        profit = round(profit, 2)
        return"-" + str(profit) + "%🔴"
    else:
        return"No change"

def twitter_pushbullet(str):
    print(str)
    push = pb.push_note("RandomTradeBot", str)
    twitter_api.update_status(str)

def update_history(money):
    day = date.today()
    date_month = str(day.day) + "/" + str(day.month)
    with open("history.txt", 'a') as f:
        line = date_month + ";" + str(money) + ";" + symbol
        f.write(line)
        f.write('\n')

#function that buys the stock
def buy(symbol):
    alpaca_api.close_all_positions()
    time.sleep(10)
    account = alpaca_api.get_account()
    money = int(float(account.cash))
    profit_message = profit(money)
    if money != 0:
        alpaca_api.submit_order(
            symbol = symbol,
            notional = money,
            side='buy',
            type='market',
            time_in_force= "day")
        twitter_pushbullet("Bought " + str(money) + " USD of " + rows[numero_random][1] + " $" + symbol +"\n" + profit_message)
        update_history(money)
    else:
        print("Error: money = 0")

buy(symbol)
"""
#uncomment this code when the code is running 24/7
while True:
    if clock.is_open :
        buy(symbol)
            
    time.sleep(86400)
"""
