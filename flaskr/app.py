import os
import random
import string
import uuid
import certifi

from flask import Flask, jsonify,request
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from pymongo import MongoClient

app = Flask(__name__)

# Replace with your Twilio Account SID and API Key SID and Secret
TWILIO_ACCOUNT_SID = 'ACcd92d71a93040dda88b5f944f37e3e7f'
TWILIO_API_KEY_SID = 'SK5e3eb4d5329ccb90aca135148413063e'
TWILIO_API_KEY_SECRET = 'EuoMnhF9jatoLrlNIRByDtz3WxX5ajgV'

conn = MongoClient('mongodb+srv://ricky:ricky123@cluster0.0gzwr1n.mongodb.net/test',tlsCAFile=certifi.where())
db = conn['dev']
userm = db.users_myngl

# @app.route('/getname',methods=['POST'])
# def getname():
#     firstname = request.form.get('firstname')

#     if(userm.find_one({'name':str(firstname)})):
#         return "Sorry that username is taken"
#     else:
#         print("Adyan before insertion")
#         userm.insert_one({'name':str(firstname)})
#         print("Adyan after insertion")
    
#     return firstname



@app.route('/token')
def token():

    print("1")
  # Create a unique ID for the client
    identity = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
    # Create an Access Token
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY_SID, TWILIO_API_KEY_SECRET, identity=identity)
    print("token correct")
    # Set the Room name
    user_id = str(uuid.uuid4())
    users_length = userm.count_documents({})
    print("Collection Length:",users_length)

    if(users_length%2==0):
        room_name = str(uuid.uuid4())
        userm.insert_one({'_id':user_id,'room_name':room_name})
    else:
        room_name = [i for i in userm.find()][-1]['room_name']
        userm.insert_one({'_id':user_id,'room_name':room_name})
    print("Room Name:",room_name)

    
    token.add_grant(VideoGrant(room=room_name))
    # Serialize the token as a JWT
    jwt = token.to_jwt()
    return jsonify(token=jwt,roomName =room_name,useractive=users_length)


