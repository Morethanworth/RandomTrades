import csv
import random
import alpaca_trade_api as tradeapi
import time
import yaml


CONFIG_FILE = 'auth.yaml'

with open(CONFIG_FILE, 'r') as config_file:
    config = yaml.safe_load(config_file)
    API_KEY_ID = config['alpaca']['API_KEY_ID']
    SECRET_KEY = config['alpaca']['SECRET_KEY']
    APCA_API_BASE_URL = config['alpaca']['APCA_API_BASE_URL']


with open('constituents_csv.csv', 'r') as file:
    reader = csv.reader(file)
    rows = []
    for row in reader:
        rows.append(row)

numero_random = random.randrange(1,len(rows))
simbolo = rows[numero_random][0]

api = tradeapi.REST(API_KEY_ID, SECRET_KEY, APCA_API_BASE_URL)

clock = api.get_clock()

def comprar(simbolo,dinheiro_investido):
    api.close_all_positions()
    time.sleep(2)
    account = api.get_account()
    dinheiro = int(float(account.buying_power))
    if dinheiro > dinheiro_investido:
        percentagem_lucro = (dinheiro/dinheiro_investido * 100)-100
        percentagem_lucro = round(percentagem_lucro, 2)
        print("Lucrei " + str(percentagem_lucro) + "%")
    elif dinheiro < dinheiro_investido:
        percentagem_lucro = (dinheiro_investido /dinheiro * 100)-100
        percentagem_lucro = round(percentagem_lucro, 2)
        print("Perdi " + str(percentagem_lucro) + "%")
    else:
        print("Fiquei na mesma\n")
    if dinheiro != 0:
        api.submit_order(
            symbol = simbolo,
            notional = dinheiro,
            side='buy',
            type='market',
            time_in_force= "day")
        print("Comprei " + str(dinheiro) + " dollars de " + simbolo)
    else:
        print("Erro: dinheiro = 0")

dinheiro_investido = 200000


comprar(simbolo,dinheiro_investido)

while True:
    if clock.is_open :
        comprar(simbolo,dinheiro_investido)
        time.sleep(86400)
