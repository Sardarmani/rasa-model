from sanic import Blueprint, response
from sanic.request import Request
from typing import Text, Dict, Any
from rasa.core.channels.channel import InputChannel, UserMessage, OutputChannel
from rasa.core.channels.channel import CollectingOutputChannel

class CustomConnector(InputChannel):
    @classmethod
    def name(cls) -> Text:
        return "custom_connector"

    async def _handle_message(self, text: Text, output_channel: OutputChannel, sender_id: Text) -> None:
        user_message = UserMessage(text, output_channel, sender_id)
        await self.on_new_message(user_message)

    def blueprint(self, on_new_message):
        custom_webhook = Blueprint("custom_webhook", __name__)

        @custom_webhook.route("/webhook", methods=["POST"])
        async def receive(request: Request):
            sender_id = request.json.get("sender")  # sender id
            text = request.json.get("message")  # message text
            output_channel = CollectingOutputChannel()
            await self._handle_message(text, output_channel, sender_id)
            return response.json({"status": "success"})

        @custom_webhook.route("/send_reminder", methods=["POST"])
        async def send_reminder(request: Request):
            sender_id = request.json.get("sender_id")
            reminder_text = request.json.get("reminder_text")
            output_channel = CollectingOutputChannel()
            await self._handle_message(reminder_text, output_channel, sender_id)
            return response.json({"status": "reminder sent"})

        return custom_webhook
