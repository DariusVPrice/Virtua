
import time 
import os
import openai
import sinch
from openai import OpenAI
from sinch import SinchClient
from flask import Flask, request

app = Flask(__name__)
# DGPW4EPS4EUJQ7UNRWH6BSAU

# sinch send
sinch_client = SinchClient(
key_id="9398bec7-4b6d-4bd0-8f41-dc7b1924d5e9",
key_secret="8KxutGfZw-CLfAu3e13Zg~RqaS",
project_id="9b3fd919-2fee-4365-86f2-c7864451810d"
)

client = OpenAI(api_key=os.environ.get("OPEN_API_KEY","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"))

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

    if all(key in inbound_message for key in ["body", "12166003244", "12085815118"]):
        sinch_client.sms.batches.send(
            body="Thank you for using the Sinch SDK. You sent: " + inbound_message["body"],
            delivery_report="none",
            to=[inbound_message["12085815118"]],
            from_=inbound_message["12166003244"]
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
    to=["12166003244"],
    from_="12085815118",
    delivery_report="none"
)
#print(send_batch_response)


