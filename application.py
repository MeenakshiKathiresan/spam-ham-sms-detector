from flask import Flask, request,render_template, make_response
from twilio import twiml
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import boto3
import datetime

import pickle
import os
application = Flask(__name__)


dynamodb = boto3.resource(
'dynamodb',
aws_access_key_id = 'AKIATANMVGXXZPKKFQFL',
aws_secret_access_key = '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',
region_name='us-east-1'
)

@application.route("/")
def index():
    message = 'Congratulations! $500 claim now !' 
    new_model_file = open('model.pkl', 'rb')
    new_model=pickle.load(new_model_file)
    prediction = (new_model.predict([message])[0], max(new_model.predict_proba([message])) * 100)
    return str(prediction)


@application.route("/", methods=['GET', 'POST'])
def sms_reply():
    sender = request.form['From']
    message = request.form['Body']

    new_model_file = open('model.pkl', 'rb')
    new_model=pickle.load(new_model_file)
    prediction = (new_model.predict([message])[0])

 
    table = dynamodb.Table('sms_classification_logs')
        
    table.put_item(
            Item={
    'Message': message,
    'Prediction': prediction,
    'Sender': sender,
    'DateTime': str(datetime.datetime.now())
        }
    )

    prediction = "The message sent is predicted as " + prediction 

    resp = MessagingResponse()
    resp.message(str(prediction))

    return str(resp)

if __name__ == "__main__":
   application.run(host='0.0.0.0', port=5000, debug=True)