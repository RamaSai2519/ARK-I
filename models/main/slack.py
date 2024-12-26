import pytz
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from shared.configs import CONFIG as config


class SlackManager:
    def __init__(self) -> None:
        self.client = WebClient(token=config.SARATHI_SLACK_BOT_TOKEN)
        self.channel = "C086BLS91K8"
        self.timezone = pytz.timezone("Asia/Kolkata")

    def join_channel(self) -> None:
        try:
            self.client.conversations_join(channel=self.channel)
        except SlackApiError as e:
            print(f"Error joining channel: {e}")

    def compose_message(self, phoneNumber: str, details: str) -> list:
        details_block = {
            "type": 'section',
            "text": {
                "type": 'mrkdwn',
                "text": f'*Details:* \n{details}',
            },
        }

        blocks = [
            {
                "type": 'section',
                "fields": [
                    {
                        "type": 'mrkdwn',
                        "text": f'*User:*\n{phoneNumber}'
                    },
                ],
            },
            details_block,
            {
                "type": 'section',
                "fields": [
                    {
                        "type": 'mrkdwn',
                        "text": f'*Time:*\n{datetime.now(self.timezone).strftime("%Y-%m-%d %H:%M:%S")}'
                    },
                ],
            }
        ]
        return blocks

    def send_message(self, phoneNumber: str, details: str) -> None:
        blocks = self.compose_message(phoneNumber, details)
        message = f"User: *{phoneNumber}* needs help with the following:"
        try:
            self.join_channel()
            response = self.client.chat_postMessage(
                channel=self.channel,
                blocks=blocks,
                text=message
            )
            if response["ok"]:
                message = "Message sent successfully"
            else:
                message = "Message failed to send" + response
            return message

        except SlackApiError as e:
            print(f"Error: {e}")
            return f"Error sending status message: {e.response['error']}"
