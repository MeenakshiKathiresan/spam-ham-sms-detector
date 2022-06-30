from flask import Flask, request,render_template, make_response
from twilio.rest import Client
from twilio import twiml
import pickle
import os

app = Flask(__name__)

@app.route("/", methods=['POST'])
def index():

    message = 'Hey there!' 

    sender = request.form['From']
    message = request.form['Body']

    new_model_file = open('model.pkl', 'rb')
    new_model=pickle.load(new_model_file)

    prediction = (new_model.predict([message])[0], max(new_model.predict_proba([message])) * 100)

    resp = twiml.Response()
    resp.message(prediction)

    return str(resp)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=4000, debug=True)
