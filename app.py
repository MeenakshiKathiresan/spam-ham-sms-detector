from flask import Flask, request,render_template, make_response
from twilio.rest import Client
import pickle
import os

app = Flask(__name__)

@app.route("/")
def index():
    message = 'Hey there!' #twilio_api.messages.stream()

    #message = request.values.get('Body', None)
    #sender = request.values.get('From', None)

    new_model_file = open('model.pkl', 'rb')
    new_model=pickle.load(new_model_file)

    prediction = (new_model.predict([message])[0], max(new_model.predict_proba([message])) * 100)
    #reply = <Response><Message> prediction </Response></Message>
    reply = prediction
    return render_template('index.html', prediction=prediction, sms=message) 

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=4000, debug=True)
