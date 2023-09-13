import slack
from flask import Flask
import threading
from slackeventsapi import SlackEventAdapter

from tokens import tokens
from eliza import JeremyChatAgent

SLACK_TOKEN = tokens.get('SLACK_TOKEN', "<TOKEN GOES HERE>")
SIGNING_SECRET = tokens.get('SIGNING_TOKEN', "<TOKEN GOES HERE>")


if SLACK_TOKEN == "<TOKEN GOES HERE>" or SIGNING_SECRET == "SIGNING_SECRET":
    print("Unable to Start")
    quit

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)

client = slack.WebClient(token=SLACK_TOKEN)

# Agent History
agents = {}

# mutex
lock = threading.Lock()


@ slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
 
    lock.acquire()

    if text == "START":
        agents[user_id] = JeremyChatAgent()
        client.chat_postMessage(channel=channel_id, text="How are you today?")
    
    elif agents.get(user_id) != None:
        response = agents[user_id].reply(text)
        client.chat_postMessage(channel=channel_id, text=response)
    
    lock.release()


if __name__ == "__main__":
    app.run(debug=True)