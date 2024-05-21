# imports omitted

client = OpenAI(api_key=os.environ.get("OPEN_API_KEY","API_KEY_HERE"))

#Local User data
current_time = time.ctime()
user_name = ""
girlfriend_name = ""
user_message = input()


#Incoming Code, This block is from Sinch API to handle incoming messages
@app.route('/', methods=['POST'])
def result():
    inbound_message = request.get_json()
    print(inbound_message)

    if all(key in inbound_message for key in ["body", "to", "from"]):
        sinch_client.sms.batches.send(
            body="Thank you for using the Sinch SDK. You sent: " + inbound_message["body"],
            delivery_report="none",
            to=[inbound_message["from"]],
            from_=inbound_message["to"]
        )

        return "Inbound message received", 200

    else:
        return "Invalid data", 400

#ChatGPT response
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

#Send code, also from sinch, to and from numbers omitted
send_batch_response = sinch_client.sms.batches.send(
    body= response.choices[0].message.content,
    to= [""],
    from_="",
    delivery_report="none"
)
print(send_batch_response)
