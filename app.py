import os
# Use the package we installed
from slack_bolt import App

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.event("reaction_added")
def handle_reaction_added_events(client, payload, event, logger, say):
  print(client.conversations_history)
  say("reaction added. event => " + str(event))
    


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

