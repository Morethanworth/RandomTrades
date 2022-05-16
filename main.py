import csv
import random
import alpaca_trade_api as tradeapi

API_KEY_ID = "PKFFMUICOK45Q9JLX0KZ"
SECRET_KEY = "jrgZrwXJ62ChrIsbTlfI2sHxTcXiGyFK6n5ccTXz"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"


with open('constituents_csv.csv', 'r') as file:
    reader = csv.reader(file)
    rows = []
    for row in reader:
        rows.append(row)

numero_random = random.randrange(1,len(rows))
simbolo = rows[numero_random][0]

api = tradeapi.REST(API_KEY_ID, SECRET_KEY, APCA_API_BASE_URL)

def comprar(simbolo,dinheiro_investido):
    api.cancel_all_orders()
    account = api.get_account()
    dinheiro = account.buying_power
    if (int(dinheiro) > dinheiro_investido):
        percentagem_lucro = (int(dinheiro)/dinheiro_investido) * 100
        print("\nLucrei " + str(percentagem_lucro) + "%")
    elif (int(dinheiro) < dinheiro_investido):
        percentagem_lucro = (dinheiro_investido / int(dinheiro)) * 100
        print("\nPerdi " + str(percentagem_lucro) + "%")
    else:
        print("\nFiquei na mesma")
    if int(dinheiro) != 0:
        api.submit_order(
            symbol = simbolo,
            notional = dinheiro,
            side='buy',
            type='market',
            time_in_force= "day")
        print("\nComprei " + dinheiro + " dollars de " + simbolo)
        dinheiro_investido = dinheiro
    else:
        print("Erro: dinheiro = 0")
    return dinheiro_investido

dinheiro_investido = 200000
comprar(simbolo,dinheiro_investido)