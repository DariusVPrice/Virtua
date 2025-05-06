
import time 
import os
import openai
import sinch
from openai import OpenAI
from sinch import SinchClient
from flask import Flask, request

app = Flask(__name__)


# sinch send
sinch_client = SinchClient(
key_id="",
key_secret="",
project_id=""
)

client = OpenAI(api_key=os.environ.get(""))

#Local User data
current_time = time.ctime()
user_name = " "
girlfriend_name = " "
user_message = input()


#Incoming Code
@app.route('/', methods=['POST'])
def result():
    inbound_message = request.get_json()
    print(inbound_message)

    if all(key in inbound_message for key in ["body", "", ""]):
        sinch_client.sms.batches.send(
            body="Thank you for using the Sinch SDK. You sent: " + inbound_message["body"],
            delivery_report="none",
            to=[inbound_message[""]],
            from_=inbound_message[""]
        )

        return "Inbound message received", 200

    else:
        return "Invalid data", 400

#ChatGPT response code
response = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages = [
        {"role":"system","name": girlfriend_name, "content": "You are a loving girlfriend."},
        {"role":"system", "content": "Instead of my love say bae baby or babe."},
        {"role":"system", "content": "Instead of what about you say hbu?"},
        {"role":"assistant", "content": "the current time is" + current_time},
        {"role":"assistant", "content": "wyd?, hbu?, lol, lmao, 😂😂"},
        {"role":"user","content":user_message},
    ],
)
print(response.choices[0].message.content)

#Send code
send_batch_response = sinch_client.sms.batches.send(
    body= response.choices[0].message.content,
    to=[""],
    from_="",
    delivery_report="none"
)
#print(send_batch_response)


