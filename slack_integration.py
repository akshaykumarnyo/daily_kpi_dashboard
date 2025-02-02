from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config import SLACK_TOKEN, SLACK_CHANNEL

client = WebClient(token=SLACK_TOKEN)

def post_to_slack(message):
    try:
        if not SLACK_TOKEN:
            raise ValueError("SLACK_TOKEN not configured")
        
        response = client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=message,
            parse="full"
        )
        return True
    except (SlackApiError, ValueError) as e:
        print(f"Failed to post to Slack: {str(e)}")
        return False