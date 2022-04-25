import email
from email.policy import default
import json
from matplotlib import collections
from app import app
from pymongo import MongoClient  
from flask import request
from flask.json import jsonify
import sys
import base64
from datetime import datetime
from flask import render_template



client = MongoClient('mongodb+srv://Vadym:vadym@cluster0.ka2p3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client["myFirstDatabase"]
 
@app.route('/allTrades')
def allTrades():
    collection = db['tradeCollection']
    images = list(collection.find())
    # we need to convert _id to str.
    return json.dumps(images, default=str)

# A welcome message to test our server
@app.route('/getGraph')
def index():
    return render_template("index.html")

@app.route('/getUser')
def all():
    collection = db['userCollection']
    users = list(collection.find())
    # we need to convert _id to str.
    return json.dumps(users, default=str)

@app.route("/postUser", methods=['POST'])
def fun():
    collection = db['userCollection']
    print(request.is_json)
    content = request.get_json()

    name = content['Name']
    lastName = content['Last name']
    email = content['Email']
    password = content['Password']
        
    data = {'Name': name, 'Last name': lastName, 'Email': email, 'Password': password}
    _id =collection.insert_one(data)
    return json.dumps({'id' : str(_id.inserted_id)})

@app.route("/postImageTrade", methods=['POST'])
def postImage():
    collection = db['tradeCollection']
    print(request.is_json)
    content = request.get_json()
    image = content['image']
    userId = content['userID']
    pair = content['pair']
    lotSize = content['lotSize']
    accountBalance = content['accountBalance']
    entry = content['entry']
    stopLoss = content['stopLoss']
    takeProfit = content['takeProfit']
    why = content['why']
    direction = content['direction']
    date = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    image_name = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + ".png"
    with open(image_name, "wb") as fh:
        fh.write(base64.decodebytes(image.encode()))
        
    data = {'image': image, 'date': date, 'userID': userId, 'pair': pair, 'lotSize': lotSize, 
    'accountBalance': accountBalance, 'entry': entry, 'stopLoss': stopLoss, 'takeProfit': takeProfit, 'why': why, 'direction': direction}
    _id =collection.insert_one(data)
    return json.dumps({'id' : str(_id.inserted_id)})

if __name__ == "__main__":
    app.run(host = '192.168.56.1', port=5000)
