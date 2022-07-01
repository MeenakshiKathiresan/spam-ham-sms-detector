from flask import Flask, request,render_template, make_response
from twilio import twiml
from twilio.twiml.messaging_response import MessagingResponse

import pickle
import os
application = Flask(__name__)

@application.route("/")
def index():
    message = 'Congratulations! $500 claim now !' 
    new_model_file = open('model.pkl', 'rb')
    new_model=pickle.load(new_model_file)
    prediction = (new_model.predict([message])[0], max(new_model.predict_proba([message])) * 100)
    return str(prediction)

@application.route("/", methods=['GET', 'POST'])
def sms_reply():
    #sender = request.form['From']
    message = request.form['Body']

    new_model_file = open('model.pkl', 'rb')
    new_model=pickle.load(new_model_file)
    prediction = (new_model.predict([message])[0])

    resp = MessagingResponse()
    resp.message(str(prediction))

    return str(resp)

if __name__ == "__main__":
   application.run(host='0.0.0.0', port=5000, debug=True)