import logging
import os
import json

from flask import Flask
from flask_ask import Ask, request, session, question, statement

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

STATUSON = ['on','high']
STATUSOFF = ['off','low']

@ask.launch
def launch():
    speech_text = 'Welcome to Raspberry Pi Automation.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)

@ask.intent('OvenIntent', mapping = {'status':'status'})
def Gpio_Intent(status,room):
    with open('./status.json') as json_file:
        data = json.load(json_file) 
    if status in STATUSON:
        if data['ovenStatus']:
            return statement('oven is already on')
        else:
            data['ovenStatus'] = 1
            with open('./status.json', 'w') as json_file:
                json.dump(data, json_file)
            return statement('turning {} Oven'.format(status))
    elif status in STATUSOFF:
        with open('./status.json') as json_file:
            data = json.load(json_file) 
        if not data['ovenStatus']:
            return statement('oven is already off')
        else:
            data['ovenStatus'] = 0
            with open('./status.json', 'w') as json_file:
                json.dump(data, json_file)
            return statement('turning {} oven'.format(status))
    else:
        return statement('Sorry not possible.')
 
@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True, port=5555)