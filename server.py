import os
import openai
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack import WebClient
from slack_bolt import App

# TODO: rename .env.example
# OPENAI_API_KEY="sk-......."
# SLACK_BOT_APP_TOKEN="xapp-......."
# SLACK_API_KEY="xoxb-......." (SLACK_APP_TOKEN)
slack_app_token = os.environ['SLACK_BOT_APP_TOKEN']
slack_bot_token = os.environ['SLACK_API_KEY']

# Event API & Web API
app = App(token=slack_bot_token) 
client = WebClient(slack_bot_token)

# This gets activated when the bot is tagged in a channel    
@app.event("app_mention")
def handle_message_events(body, logger):
    # Log message
    print(str(body["event"]["text"]).split(">")[1])
    
    # Create prompt for ChatGPT
    prompt = str(body["event"]["text"]).split(">")[1]
    
    # Let thre user know that we are busy with the request 
    response = client.chat_postMessage(channel=body["event"]["channel"], 
                                       thread_ts=body["event"]["event_ts"],
                                       text=f"Hello from your bot! :robot_face: \nThanks for your request, I'm on it!")
    
    # Check ChatGPT
    openai.api_key = os.environ['OPENAI_API_KEY']
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5).choices[0].text
    
    
    # Reply to thread 
    response = client.chat_postMessage(channel=body["event"]["channel"], 
                                       thread_ts=body["event"]["event_ts"],
                                       text=f"Here you go: \n{response}")

if __name__ == "__main__":
    SocketModeHandler(app, slack_app_token).start()