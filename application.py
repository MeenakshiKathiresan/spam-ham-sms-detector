from flask import Flask, request,render_template, make_response
from twilio import twiml
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import boto3
import datetime
from boto3.dynamodb.conditions import Key

import pickle
import os
application = Flask(__name__)


dynamodb = boto3.resource(
'dynamodb',
aws_access_key_id = '',
aws_secret_access_key = '',
region_name='us-east-1'
)

@application.route("/")
def index():
    message = 'Congratulations! $500 claim now !' 
    new_model_file = open('ML model/model.pkl', 'rb')
    new_model=pickle.load(new_model_file)
    prediction = (new_model.predict([message])[0], max(new_model.predict_proba([message])) * 100)
    return str(prediction)


@application.route("/", methods=['GET', 'POST'])
def sms_reply():
    sender = request.form['From']
    message = request.form['Body']
    table = dynamodb.Table('sms_classification_logs')

    response = table.query(
            KeyConditionExpression=Key('Sender').eq(sender)
            )

    items = response['Items']
    valid_msg = ""

    clean_msg = message.strip().lower()

    # Validation message sent by user
    if len(items)>0 and (clean_msg == 'correct' or clean_msg == 'wrong'):

        # get last item
        last_item = items[len(items)-1]
        valid_msg = last_item['Validation']

        # check if validation message field is empty
        if valid_msg == '':

            if clean_msg == 'correct':
                prediction = "Thank you for confirming."
            elif clean_msg == 'wrong':
                prediction = "Oops! Thank you for helping us get better."

            # override last entry with validation message
            table.put_item(Item={
                'Validation': message, 
                'Sender': sender, 
                'DateTime': last_item['DateTime'],
                'Message':last_item['Message'] ,
                'Prediction': last_item['Prediction']})

    else:

        # prediction
        new_model_file = open('model.pkl', 'rb')
        new_model=pickle.load(new_model_file)
        prediction = (new_model.predict([message])[0])

        # new row on dynamodb
        table.put_item(
                Item={
        'Message': message,
        'Prediction': prediction,
        'Sender': sender,
        'DateTime': str(datetime.datetime.now()),
        'Validation': ''
            }
        )

        # prediction message
        prediction = "The message sent is predicted as " + prediction + "\nValidate by sending 'correct' or 'wrong'."

    # send back response
    resp = MessagingResponse()
    resp.message(str(prediction))

    return str(resp)

if __name__ == "__main__":
   application.run(host='0.0.0.0', port=5000, debug=True)