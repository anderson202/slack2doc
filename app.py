import os
# Use the package we installed
from slack_bolt import App
from slack_sdk.errors import SlackApiError
from datetime import datetime

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.event("reaction_added")
def handle_reaction_added_events(client, payload, event, logger, say):
  reaction = event["reaction"]

  if reaction != "pushpin":
      return

  event_item = event["item"]
  event_channel, event_timestamp = "", ""

  if event_item["type"] == "message":
      event_channel = event_item["channel"]
      event_timestamp = event_item["ts"]
      messages = _fetch_conversation(client, event_channel, event_timestamp)
      if len(messages) > 0:
        formatted = _format_messages(client, messages)
        say("here's your saved thread: \n" + formatted)
  else:
      say("message cannot be saved")

def _fetch_conversation(client, conversation_id, timestamp):
    try:
        # Call the conversations.history method using the WebClient
        # The client passes the token you included in initialization    
        result = client.conversations_history(
            channel=conversation_id,
            inclusive=True,
            oldest=timestamp,
            limit=1
        )
        message = result["messages"][0]
        print(str(message))
        if _is_thread_parent(message["thread_ts"], message["ts"]):
            print("is thread parent, trying to find all replies")
            result = client.conversations_replies(
                ts=message["thread_ts"],
                channel=conversation_id,
                limit=200,
            )

            saved_message = []
            if len(result["messages"]) > 0:
                for message in result["messages"]:
                    saved_message.append(message)

            return saved_message
            
        else:
            print("not thread parent")
            return []

    except SlackApiError as e:
        print(f"Error: {e}")

def _is_thread_parent(thread_ts, ts):
    return thread_ts == ts

def _format_messages(client, messages):
    print(messages)
    formatted_str = ""

    formatted_str += "```\n"

    for message in messages:
        result = client.users_info(
            user=message["user"]
        )
        
        user = result["user"]
        formatted_str += message["text"] + " - " + user["real_name"] + " @ " + str(datetime.fromtimestamp(float(message["ts"]))) + "\n"
    
    formatted_str += "```"

    return formatted_str
    


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

