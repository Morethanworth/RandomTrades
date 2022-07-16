import csv
import time
import tweepy
import random
import yaml
import alpaca_trade_api as tradeapi
from datetime import date
from pushbullet import Pushbullet
import urllib.request
import json


history_file = 'history.txt'

def get_jsonparsed_data(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    return json.loads(data)

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


def profits(money_now,money_before):
    if money_now == 0:
        return " "
    #insert here your starting money
    if money_now > money_before:
        profit = ((money_now/money_before) * 100) - 100
        profit = round(profit, 2)
        return "+" + str(profit) + "%🟢\n"
    elif money_now < money_before:
        profit = ((money_before /money_now) * 100)-100
        profit = round(profit, 2)
        return"-" + str(profit) + "%🔴\n"
    else:
        return"no change\n"


def money_yesterday():
    with open('history.txt') as f:
        last_line = f.readlines()[-1]
        money = last_line.split(";")
    
    return money[1]


def twitter_pushbullet(str):
    print(str)
    push = pb.push_note("RandomTradeBot", str)
    tweet = twitter_api.update_status_with_media(str, "logo.png")
    twitter_api.update_status(status,in_reply_to_status_id=tweet.id)
    

def update_history(money):
    day = date.today()
    date_month = str(day.day) + "/" + str(day.month)
    with open("history.txt", 'a') as f:
        line = date_month + ";" + str(money) + ";" + symbol
        f.write(line)
        f.write('\n')   

#function that buys the stock
def buy(symbol):
    yesterday_money = money_yesterday()
    alpaca_api.close_all_positions()    
    time.sleep(10)
    account = alpaca_api.get_account()
    money = int(float(account.cash))
    profit_message_begin = profits(money,100000)
    profit_yesterday = profits(money,int(yesterday_money))
    if money != 0:
        alpaca_api.submit_order(
            symbol = symbol,
            notional = money,
            side='buy',
            type='market',
            time_in_force= "day")
        twitter_pushbullet("Bought " + str(money) + " USD of " + rows[numero_random][1] + " $" + symbol + "\n" + "Change all time:" + 
                                profit_message_begin + "Change yesterday:" + profit_yesterday )
        update_history(money)
    else:
        print("Error: money = 0")

#buy(symbol)

url = ("https://financialmodelingprep.com/api/v3/profile/" + symbol + "?apikey=c4d832fff8d794cf22fe3684211f7cb8")
data = get_jsonparsed_data(url)
address = data[0]["address"]
city = data[0]["city"]
state = data[0]["state"]
price = data[0]["price"]
industry = data[0]["industry"]
website = data[0]["website"]
ceo = data[0]["ceo"]
employees = data[0]["fullTimeEmployees"]
imageurl = data[0]["image"] 
urllib.request.urlretrieve(imageurl, "logo.png")
status = "STOCK INFO\nIndustry: " + industry + "\nStock price: " + str(price) + "$" +  "\nAddress: " + address + ", "+ city + ", "+ state + "\nCEO: " + ceo + "\nNumber of employees: " + employees + "\n" + website
twitter_pushbullet("OI")
"""
#uncomment this code when the code is running 24/7
while True:
    if clock.is_open :
        buy(symbol)
            
    time.sleep(86400)
"""
