import os
import warnings
from flask import Flask, render_template, make_response
from twilio.rest import Client
#from dotenv import load_dotenv
from model import load_model,  process_sms

#load_dotenv()  # load environment variables

TWILIO_ACCOUNT_SID = "ACf243fe2d03b949f9e2c766127334c958"#os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = "5452df78247e6de398593437a59f3d01"#os.environ["TWILIO_AUTH_TOKEN"]
twilio_api = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

warnings.filterwarnings("ignore")

app = Flask(__name__)

def get_sms_and_predict(start, end):
    '''
    Return predictions for the sms between start and end.
    This is efficient for paginations
    '''
    model = load_model()  # load saved model
    sms = list(twilio_api.messages.stream())
    if (end > len(sms)):
        end = len(sms)

    sub_sms = sms[start:end]
    spam_msg = []
    not_spam_msg = []
    for msg in sub_sms:
        txt = msg.body
        txt = process_sms(txt)
        pred = (model.predict(txt) > 0.5).astype("int32").item()

        if pred == 1:
            spam_msg.append(msg)
        else:
            not_spam_msg.append(msg)
    return spam_msg, not_spam_msg

@app.route("/")
def index():
    spam_msg, not_spam_msg = get_sms_and_predict(0, 5)
    template = render_template('index.html', spam_msg=spam_msg, not_spam_msg=not_spam_msg)
    response = make_response(template)
    return response

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=4000, debug=True)