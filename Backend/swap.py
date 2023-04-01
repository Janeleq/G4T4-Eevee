from invokes import invoke_http
from flask import Flask, request, jsonify
import os, json
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/swap", methods = ['GET'])
def swap():
    if request.method == 'GET':
        from_amount = request.args.get('from_amount')
        from_currency = request.args.get("from_currency")
        to_currency = request.args.get("to_currency")

        from_price_URL = f"http://127.0.0.1:5001/coin/{from_currency}"
        to_price_URL = f"http://127.0.0.1:5001/coin/{to_currency}"
        # wallet_URL = ""

        conversion_ratio = getRatio(from_price_URL, to_price_URL)

        # Retrieves wallet balance 
        # wallet_data = invoke_http(wallet_URL, 'GET', json=EMAIL)

        conversion_amount = from_amount * conversion_ratio

        #Updates wallet

        # #Status of failed swap
        # if <> not in range(200, 300):
        #     #AMQP activity

            
        #     return {
        #         "code": 500,
        #         "message": "Swap failure sent for error handling."
        #     }

        #Status of successful swap
        # else:
        #     #AMQP activity

        return {
            "code": 400,
            'conversion_amount': conversion_amount
        }
    
def getPrice(response):
    price = response['data']['price']
    return price

# Obtain rates from price.py and calculates ratio of swap (to rate / from rate)

def getRatio(from_url, to_url):
    to_price_data = requests.get(to_url)
    from_price_data = requests.get(from_url)
    print(to_price_data)
    print(from_price_data)
    if to_price_data:
        to_price_data = to_price_data.json()
        to_price = getPrice(to_price_data)
    if from_price_data:
        from_price_data = from_price_data.json() 
        from_price = getPrice(from_price_data) 
    return str(from_price / to_price)

# Update wallet of new balance
def updateWallet(walletId):
    pass 

if __name__ == "__main__":
    app.run(port=5004, debug=True)
