# $ set FLASK_APP=app22
# $ set FLASK_ENV=development
# $ flask run
# $ heroku buildpacks:add heroku/python
# $ heroku logs --tail
import time
from OmerAPI import config
from OmerAPI import BinanceTrService as service
from flask import Flask,request, json
app=Flask(__name__)

client = service.ApiService(apiKey=config.akey, apiSecret=config.skey)
print(client.testConnectivity())


def order_buy(side, symbol):
        try:
            print(f"<<<<<<<<<<SENDING ORDER & BUYING'ING WITH  BUSD >>>>>>>>>>")
            order_buy = client.postBuyMarketOrder(side=side, symbol=symbol)
        except Exception as e:
            print("an exception occured - {}".format(e))
            return False
        return order_buy


def order_sell(side, symbol):
        try:
            print(f"<<<<<<<<<<SENDING ORDER & SELL'ING  {symbol}>>>>>>>>>>")
            order_sell = client.postSellMarketOrder(side=side, symbol=symbol)
        except Exception as e:
            print("an exception occured - {}".format(e))
            return False
        return order_sell

@app.route("/webhook", methods=['POST'])
def webhook():
    print(request.data)
    data = json.loads(request.data)

    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
            "code": "<<<ERROR>>>",
            "message": "<<<INVAILED PASSPHRASE>>>"
        }
    else:

        print(data['strategy'])
        print(data['bar'])
        side = data['strategy']['side'].upper()
        symbol = data['strategy']['symbol']
        order_response = order_sell(side, symbol)

        if order_response:
            print(order_response)
            print("<<<ORDER EXECUTED>>>")
            return {
                "code": "<<<SUCCESS>>>",
                "message": "<<<ORDER EXECUTED>>>"
            }
    #    else:
   #         print(order_response)
     #       print("<<<ORDER FAILED>>>")
    #        return {
     #           "code": "<<<ERROR>>>",
    #            "message": "<<<ORDER FAILED>>>"
    #        }

