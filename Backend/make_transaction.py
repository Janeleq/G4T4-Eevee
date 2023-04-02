# make_transaction complex Microservice
# have to invoke wallet.py to check wheter got enough $$ to eg buy cc defined

from flask import Flask, redirect, render_template, url_for, request, jsonify
from flask_cors import CORS
import time
import pyrebase
import os, sys
from os import environ

import requests
from invokes import invoke_http

import pika
import json

app = Flask(__name__, template_folder='../Frontend/templates', static_folder='../Frontend/static')
CORS(app)

firebase_config = {
    "apiKey": "AIzaSyAUfijsgUQsPpdx5A21wO0wCS1qRkwh5o0",
    "authDomain": "cryptobuds-ba428.firebaseapp.com",
    "databaseURL": "https://cryptobuds-ba428-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "cryptobuds-ba428",
    "storageBucket": "cryptobuds-ba428.appspot.com",
    "messagingSenderId": "72206190161",
    "appId": "1:72206190161:web:bc8dbb3bf116fcc69fda70",
    "measurementId": "G-BVXDMYJR2K"
}
fb = pyrebase.initialize_app(firebase_config)
database = fb.database()


#set up RabbitMQ Connection
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()
# channel.queue_declare(queue='buy_order_queue')
marketplace_URL = "http://localhost:5000/marketplace"
price_URL =  "http://127.0.0.1:5001" 
# buy_transaction_URL =  "http://localhost:5004/" 
# sell_transaction_URL =  "http://localhost:5004/" 

def getQty(qty):
    return qty


def getPrice(response):
    price = response['data']['price']
    price = str(price)
    return price

def getNumber(number,coin):
    number = number[coin]
    return number

# #BINANCE
@app.route("/BNB")
def binance():
    return render_template('coins/bnb.html')

#BITCOIN
@app.route("/BTC")
def bitcoin():
    return render_template('coins/btc.html')

#CARDANO
@app.route("/ADA")
def cardano():
    return render_template('coins/ada.html')

#DOGE
@app.route("/DOGE")
def doge():
    return render_template('coins/doge.html')

#ETHEREUM
@app.route("/ETH")
def ethereum():
    return render_template('coins/eth.html')

# SOLANA
@app.route("/SOL")
def solana():
    return render_template('coins/sol.html')


@app.route("/<string:coin>/buy")
def buycc(coin):
    qty = request.args.get('buyqty')
    qty = getQty(qty)
    price_URL = "http://localhost:5001" 
    price_URL = price_URL + "/coin/" + coin
    wallet_USD = "http://localhost:5100/wallet/USD"
    wallet_URL = "http://localhost:5100/wallet/" + coin
    #get price
    response = requests.get(price_URL, timeout=10)
    #get USD owned
    amount_owned = requests.get(wallet_USD, timeout=10)
    if response:
        #get total price needed to pay with current price + quantity
        response = response.json()
        price = getPrice(response)
        total_amount = round(float(qty) * float(price),2)

    if amount_owned:
        amount_owned = amount_owned.json()
        qty_usd_owned = getNumber(amount_owned, "USD")

    if qty_usd_owned >= total_amount:
        id = "DsU3Gmoe1McjyXU8JA66GfiBG7L2"
        qty_coin_owned = requests.get(wallet_URL)
        if qty_coin_owned:
            ownedcoin = qty_coin_owned.json()
            ownedcoin = getNumber(ownedcoin, coin)
            decrease = qty_usd_owned - total_amount
            increase = float(ownedcoin) + float(qty)
            database.child("users").child(id).child('wallet_coins').child("USD").update({"qty":decrease})
            database.child("users").child(id).child('wallet_coins').child(coin).update({"qty": increase})
            result = {
                "code":200,
                "message": "Transaction successful!"
            }, 200
            return result
        else:
            return "haha"
    else:
        result = {
            "code" : 400,
            "message": "Transaction failed, please try again as you do not have enough balance in your wallet to make the transaction."
        }, 400
        return result 
    




@app.route("/<string:coin>/sell")
def sellcc(coin):
    qty = request.args.get('sellqty')
    qty = getQty(qty)
    price_URL = "http://localhost:5001" 
    price_URL = price_URL + "/coin/" + coin
    wallet_USD = "http://localhost:5100/wallet/USD"
    wallet_URL = "http://localhost:5100/wallet/" + coin
    #get price
    response = requests.get(price_URL, timeout=10)

    if response:
        #get total price needed to pay with current price + quantity
        response = response.json()
        price = getPrice(response)
        total_amount = round(float(qty) * float(price),2)

    coin_owned = requests.get(wallet_URL)
    if coin_owned:
        coin_owned = coin_owned.json()
        qty_coin_owned = getNumber(coin_owned, coin)

    # if amount_owned:
    #     amount_owned = amount_owned.json()
    #     qty_usd_owned = getNumber(amount_owned, "USD")

    if qty_coin_owned >= float(qty):
        id = "DsU3Gmoe1McjyXU8JA66GfiBG7L2"
        amount_owned = requests.get(wallet_USD)
        if amount_owned:
            qty_usd_owned = amount_owned.json()
            qty_usd_owned = getNumber(qty_usd_owned, "USD")
            decrease = float(qty_coin_owned) - float(qty)
            increase = qty_usd_owned + total_amount
            database.child("users").child(id).child('wallet_coins').child("USD").update({"qty":increase})
            database.child("users").child(id).child('wallet_coins').child(coin).update({"qty": decrease})
            result = {
                "code":200,
                "message": "Transaction successful!"
            }, 200
            return result
        else:
            return "haha"
    else:
        result = {
            "code" : 400,
            "message": "Transaction failed, please try again as you do not have enough balance in your wallet to make the transaction."
        }, 400
        return result 
    
@app.route("/<string:coin>/buyorder")
def buyordercc(coin):
    qty = request.args.get('buyorderqty')
    boprice = request.args.get('buyorderprice')
    price_URL = "http://localhost:5001" 
    price_URL = price_URL + "/coin/" + coin
    response = requests.get(price_URL, timeout=10)
    if response:
        response = response.json()
        current_price = getPrice(response)
        total_amount = round(float(qty) * float(boprice),2)
        #if total_amount <= wallet balance --> place buy order
        #else --> error
        #update wallet + cryptocurrency owned
        
        return str(total_amount)

    else:
        return 0 


@app.route("/<string:coin>/sellorder")
def sellordercc(coin):
    qty = request.args.get('sellorderqty')
    soprice = request.args.get('sellorderprice')
    price_URL = "http://localhost:5001" 
    price_URL = price_URL + "/coin/" + coin
    response = requests.get(price_URL, timeout=10)
    if response:
        response = response.json()
        current_price = getPrice(response)
        total_amount = round(float(qty) * float(current_price),2)
        #if qty sold <= qty owned --> place sell order
        #else --> error
        #update wallet + cryptocurrency owned

        return str(total_amount)

    else:
        return 0 


if __name__ == '__main__':
    app.run(port=5010, debug=True)









